"""Utilities for parsing TRExFitter."""

# stdlib
import io
import logging
import math
import multiprocessing
import os
import random
import sys
from dataclasses import dataclass
from pathlib import PosixPath
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

# external
import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import uproot4 as uproot
from uproot4.reading import ReadOnlyDirectory

import yaml

# tdub
import tdub.config
from .art import (
    canvas_from_counts,
    setup_tdub_style,
    draw_atlas_label,
    draw_impact_barh,
    legend_last_to_first,
)
from .root import TGraphAsymmErrors, TH1

setup_tdub_style()

log = logging.getLogger(__name__)


@dataclass
class NuisPar:
    """Nuisance parameter description as a dataclass.

    Attributes
    ----------
    name : str
        Technical name of the nuisance parameter.
    label : str
        Pretty name for plotting.
    pre_down : float
        Prefit down variation impact on delta mu.
    pre_up : float
        Prefit up variation impact on delta mu.
    post_down : float
        Postfit down variation impact on delta mu.
    post_up : float
        Postfit up variation impact on delta mu.
    central : float
        Central value of the NP.
    sig_lo : float
        Lo error on the NP.
    sig_hi : float
        Hi error on the NP.

    """

    name: str = ""
    label: str = ""
    pre_down: float = 0.0
    pre_up: float = 0.0
    post_down: float = 0.0
    post_up: float = 0.0
    central: float = 0.0
    sig_lo: float = 0.0
    sig_hi: float = 0.0
    post_max: float = 0.0

    def __post_init__(self):
        """Execute after init."""
        self.post_max = max(abs(self.post_down), abs(self.post_up))


def available_regions(wkspace: Union[str, os.PathLike]) -> List[str]:
    """Get a list of available regions from a workspace.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace

    Returns
    -------
    list(str)
        Regions discovered in the workspace.

    """
    root_files = (PosixPath(wkspace) / "Histograms").glob("*_preFit.root")
    return [rf.name[:-12] for rf in root_files if "asimov" not in rf.name]


def data_histogram(
    wkspace: Union[str, os.PathLike], region: str, fitname: str = "tW"
) -> TH1:
    """Get the histogram for the Data in a region from a workspace.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace
    region : str
        TRExFitter region name.
    fitname : str
        Name of the Fit

    Returns
    -------
    tdub.root.TH1
        Histogram for the Data sample.

    """
    root_path = PosixPath(wkspace) / "Histograms" / f"{fitname}_{region}_histos.root"
    return TH1(uproot.open(root_path).get(f"{region}_Data"))


def chisq(
    wkspace: Union[str, os.PathLike], region: str, stage: str = "pre"
) -> Tuple[float, int, float]:
    r"""Get prefit :math:`\chi^2` information from TRExFitter region.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace
    region : str
        TRExFitter region name.
    stage : str
        Drawing fit stage, ('pre' or 'post').

    Returns
    -------
    :py:obj:`float`
        :math:`\chi^2` value for the region.
    :py:obj:`int`
        Number of degrees of freedom.
    :py:obj:`float`
        :math:`\chi^2` probability for the region.

    """
    if stage not in ("pre", "post"):
        raise ValueError("stage can only be 'pre' or 'post'")
    txt_path = PosixPath(wkspace) / "Histograms" / f"{region}_{stage}Fit_Chi2.txt"
    table = yaml.full_load(txt_path.read_text())
    return table["chi2"], table["ndof"], table["probability"]


def chisq_text(wkspace: Union[str, os.PathLike], region: str, stage: str = "pre") -> None:
    r"""Generate nicely formatted text for :math:`\chi^2` information.

    Deploys :py:func:`tdub.rex.chisq` for grab the info.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace
    region : str
        TRExFitter region name.
    stage : str
        Drawing fit stage, ('pre' or 'post').

    Returns
    -------
    str
        Formatted string showing the :math:`\chi^2` information.

    """
    chi2, ndof, prob = chisq(wkspace, region, stage=stage)
    return (
        f"$\\chi^2/\\mathrm{{ndf}} = {chi2:3.2f} / {ndof}$, "
        f"$\\chi^2_{{\\mathrm{{prob}}}} = {prob:3.2f}$"
    )


def prefit_histogram(root_file: ReadOnlyDirectory, sample: str, region: str) -> TH1:
    """Get a prefit histogram from a file.

    Parameters
    ----------
    root_file : uproot4.reading.ReadOnlyDirectory
        File containing the desired prefit histogram.
    sample : str
        Physics sample name.
    region : str
        TRExFitter region name.

    Returns
    -------
    tdub.root.TH1
        Desired histogram.

    """
    histname = f"{region}_{sample}"
    try:
        h = root_file.get(histname)
        h = TH1(root_file.get(histname))
        return h
    except KeyError:
        log.fatal("%s histogram not found in %s" % (histname, root_file))
        exit(1)


def prefit_histograms(
    wkspace: Union[str, os.PathLike],
    samples: Iterable[str],
    region: str,
    fitname: str = "tW",
) -> Dict[str, TH1]:
    """Retrieve sample prefit histograms for a region.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace
    samples : Iterable(str)
        Physics samples of the desired histograms
    region : str
        Region to get histograms for
    fitname : str
        Name of the Fit

    Returns
    -------
    dict(str, tdub.root.TH1)
        Prefit histograms.

    """
    root_path = PosixPath(wkspace) / "Histograms" / f"{fitname}_{region}_histos.root"
    root_file = uproot.open(root_path)
    histograms = {}
    for samp in samples:
        h = prefit_histogram(root_file, samp, region)
        if h is None:
            log.warn("Histogram for sample %s in region: %s not found" % (samp, region))
        histograms[samp] = h
    return histograms


def hepdata(
    wkspace: Union[str, os.PathLike], region: str, stage: str = "pre",
) -> Dict[Any, Any]:
    """Parse HEPData information.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace
    region : str
        Region to get histograms for
    stage : str
        Fitting stage (`"pre"` or `"post"`).

    """
    yaml_path = PosixPath(wkspace) / "Plots" / f"{region}_{stage}fit.yaml"
    return yaml.full_load(yaml_path.read_text())


def prefit_total_and_uncertainty(
    wkspace: Union[str, os.PathLike], region: str
) -> Tuple[TH1, TGraphAsymmErrors]:
    """Get the prefit total MC prediction and uncertainty band for a region.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace.
    region : str
        Region to get error band for.

    Returns
    -------
    :py:obj:`tdub.root.TH1`
        The total MC expectation histogram.
    :py:obj:`tdub.root.TGraphAsymmErrors`
        The error TGraph.

    """
    root_path = PosixPath(wkspace) / "Histograms" / f"{region}_preFit.root"
    root_file = uproot.open(root_path)
    err = TGraphAsymmErrors(root_file.get("g_totErr"))
    tot = TH1(root_file.get("h_tot"))
    return tot, err


def postfit_available(wkspace: Union[str, os.PathLike]) -> bool:
    """Check if TRExFitter workspace contains postFit information.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace

    Returns
    -------
    bool
        True of postFit discovered

    """
    histdir = PosixPath(wkspace) / "Histograms"
    for f in histdir.iterdir():
        if "postFit" in f.name:
            return True
    return False


def postfit_histogram(root_file: ReadOnlyDirectory, sample: str) -> TH1:
    """Get a postfit histogram from a file.

    Parameters
    ----------
    root_file : uproot4.reading.ReadOnlyDirectory
        File containing the desired postfit histogram.
    sample : str
        Physics sample name.

    Returns
    -------
    tdub.root.TH1
        Desired histogram.

    """
    histname = f"h_{sample}_postFit"
    try:
        h = TH1(root_file.get(histname))
        return h
    except KeyError:
        log.fatal("%s histogram not found in %s" % (histname, root_file))
        exit(1)


def postfit_histograms(
    wkspace: Union[str, os.PathLike], samples: Iterable[str], region: str
) -> Dict[str, TH1]:
    """Retrieve sample postfit histograms for a region.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace
    region : str
        Region to get histograms for
    samples : Iterable(str)
        Physics samples of the desired histograms

    Returns
    -------
    dict(str, tdub.root.TH1)
        Postfit histograms detected in the workspace.

    """
    root_path = PosixPath(wkspace) / "Histograms" / f"{region}_postFit.root"
    root_file = uproot.open(root_path)
    histograms = {}
    for samp in samples:
        if samp == "Data":
            continue
        h = postfit_histogram(root_file, samp)
        if h is None:
            log.warn("Histogram for sample %s in region %s not found" % (samp, region))
        histograms[samp] = h
    return histograms


def postfit_total_and_uncertainty(
    wkspace: Union[str, os.PathLike], region: str
) -> Tuple[Any, Any]:
    """Get the postfit total MC prediction and uncertainty band for a region.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace.
    region : str
        Region to get error band for.

    Returns
    -------
    :py:obj:`tdub.root.TH1`
        The total MC expectation histogram.
    :py:obj:`tdub.root.TGraphAsymmErrors`
        The error TGraph.

    """
    root_path = PosixPath(wkspace) / "Histograms" / f"{region}_postFit.root"
    root_file = uproot.open(root_path)
    err = TGraphAsymmErrors(root_file.get("g_totErr_postFit"))
    tot = TH1(root_file.get("h_tot_postFit"))
    return tot, err


def meta_text(region: str, stage: str) -> str:
    """Construct a piece of text based on the region and fit stage.

    Parameters
    ----------
    region : str
        TRExFitter Region to use.
    stage : str
        Fitting stage (`"pre"` or `"post"`).

    Returns
    -------
    str
        Resulting metadata text

    """
    if stage == "pre":
        stage = "Pre-fit"
    elif stage == "post":
        stage = "Post-fit"
    else:
        raise ValueError("stage can be 'pre' or 'post'")
    if "1j1b" in region:
        region = "1j1b"
    elif "2j1b" in region:
        region = "2j1b"
    elif "2j2b" in region:
        region = "2j2b"
    else:
        raise ValueError("region must contain '1j1b', '2j1b', or '2j2b'")
    return f"$tW$ Dilepton, {region}, {stage}"


def meta_axis_label(region: str, meta_table: Optional[Dict[str, Any]] = None) -> str:
    """Construct an axis label from metadata table.

    Parameters
    ----------
    region : str
        TRExFitter region to use.
    meta_table : dict, optional
        Table of metadata for labeling plotting axes. If ``None``
        (default), the definition stored in the variable
        ``tdub.config.PLOTTING_META_TABLE`` is used.

    Returns
    -------
    str
        Axis label for the region.

    """
    if "VRP" in region:
        region = region[12:]
    if meta_table is None:
        if tdub.config.PLOTTING_META_TABLE is None:
            raise ValueError("tdub.config.PLOTTING_META_TABLE must be defined")
        else:
            meta_region = tdub.config.PLOTTING_META_TABLE["titles"][region]
    else:
        meta_region = meta_table["titles"][region]
    main_label = meta_region["mpl"]
    unit_label = meta_region["unit"]
    if not unit_label:
        return main_label
    else:
        return f"{main_label} [{unit_label}]"


def stack_canvas(
    wkspace: Union[str, os.PathLike],
    region: str,
    stage: str = "pre",
    fitname: str = "tW",
    show_chisq: bool = True,
    meta_table: Optional[Dict[str, Any]] = None,
    log_patterns: Optional[List[Any]] = None,
) -> Tuple[plt.Figure, plt.Axes, plt.Axes]:
    r"""Create a pre- or post-fit plot canvas for a TRExFitter region.

    Parameters
    ---------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace.
    region : str
        Region to get error band for.
    stage : str
        Drawing fit stage, (`"pre"` or `"post"`).
    fitname : str
        Name of the Fit
    show_chisq : bool
        Print :math:`\chi^2` information on ratio canvas.
    meta_table : dict, optional
        Table of metadata for labeling plotting axes.
    log_patterns : list, optional
        List of region patterns to use a log scale on y-axis.

    Returns
    -------
    :py:obj:`matplotlib.figure.Figure`
        Figure for housing the plot.
    :py:obj:`matplotlib.axes.Axes`
        Main axes for the histogram stack.
    :py:obj:`matplotlib.axes.Axes`
        Ratio axes to show Data/MC.

    """
    samples = ("tW", "ttbar", "Zjets", "Diboson", "MCNP")
    if stage == "pre":
        histograms = prefit_histograms(wkspace, samples, region, fitname=fitname)
        total_mc, uncertainty = prefit_total_and_uncertainty(wkspace, region)
    elif stage == "post":
        histograms = postfit_histograms(wkspace, samples, region)
        total_mc, uncertainty = postfit_total_and_uncertainty(wkspace, region)
    else:
        raise ValueError("stage must be 'pre' or 'post'")
    histograms["Data"] = data_histogram(wkspace, region)
    bin_edges = histograms["Data"].edges
    counts = {k: v.counts for k, v in histograms.items()}
    errors = {k: v.errors for k, v in histograms.items()}

    if log_patterns is None:
        log_patterns = tdub.config.PLOTTING_LOGY
    logy = False
    for pat in log_patterns:
        if pat.search(region) is not None:
            logy = True

    fig, ax0, ax1 = canvas_from_counts(
        counts, errors, bin_edges, uncertainty=uncertainty, total_mc=total_mc, logy=logy,
    )

    # stack axes cosmetics
    ax0.set_ylabel("Events", horizontalalignment="right", y=1.0)
    draw_atlas_label(ax0, extra_lines=[meta_text(region, stage)])
    legend_last_to_first(ax0, ncol=2, loc="upper right")

    # ratio axes cosmetics
    ax1.set_xlabel(meta_axis_label(region, meta_table), horizontalalignment="right", x=1.0)
    ax1.set_ylabel("Data/MC")
    if stage == "post":
        ax1.set_ylim([0.9, 1.1])
        ax1.set_yticks([0.9, 0.95, 1.0, 1.05])
    if show_chisq:
        ax1.text(
            0.02, 0.8, chisq_text(wkspace, region, stage), transform=ax1.transAxes, size=11
        )
    ax1.legend(loc="lower left", fontsize=11)

    # return objects
    return fig, ax0, ax1


def plot_region_stage_ff(args):
    """Free (multiprocessing compatible) function to plot a region + stage.

    This function is designed to be used internally by
    :py:func:`plot_all_regions`, where it is sent to a multiprocessing
    pool. Not meant for generic usage.

    Parameters
    ----------
    args: list(Any)
        Arguments passed to :py:func:`stack_canvas`.

    """
    fig, ax0, ax1 = stack_canvas(
        wkspace=args[0],
        region=args[1],
        stage=args[3],
        show_chisq=args[4],
        meta_table=args[5],
        log_patterns=args[6],
    )
    output_file = f"{args[2]}/{args[1]}_{args[3]}Fit.pdf"
    fig.savefig(output_file)
    plt.close(fig)
    del fig, ax0, ax1
    log.info("Created %s" % output_file)


def plot_all_regions(
    wkspace: Union[str, os.PathLike],
    outdir: Union[str, os.PathLike],
    stage: str = "pre",
    fitname: str = "tW",
    show_chisq: bool = True,
    n_test: int = -1,
) -> None:
    r"""Plot all regions discovered in a workspace.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace
    outdir : str or os.PathLike
        Path to save resulting files to
    stage : str
        Fitting stage (`"pre"` or `"post"`).
    fitname : str
        Name of the Fit
    show_chisq : bool
        Print :math:`\chi^2` information on ratio canvas.
    n_test : int
        Maximum number of regions to plot (for quick tests).

    """
    PosixPath(outdir).mkdir(parents=True, exist_ok=True)
    regions = available_regions(wkspace)
    if n_test > 0:
        regions = random.sample(regions, n_test)
    meta_table = tdub.config.PLOTTING_META_TABLE.copy()
    log_patterns = tdub.config.PLOTTING_LOGY.copy()
    args = [
        [wkspace, region, outdir, stage, show_chisq, meta_table, log_patterns]
        for region in regions
    ]
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(plot_region_stage_ff, args)


def nuispar_impact(
    wkspace: Union[str, os.PathLike], name: str, label: Optional[str] = None
) -> NuisPar:
    """Extract a specific nuisance parameter from a fit.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace.
    name : str
        Name of the nuisance parameter.
    label : str, optional
        Give the nuisance parameter a label other than its name.

    Returns
    -------
    tdub.rex.NuisPar
        Desired nuisance parameter summary.

    """
    n, c, su, sd, postup, postdn, preup, predn = (
        (PosixPath(wkspace) / "Fits" / f"NPRanking_{name}.txt").read_text().strip().split()
    )
    npar = NuisPar(
        name,
        name,
        round(float(predn), 6),
        round(float(preup), 6),
        round(float(postdn), 6),
        round(float(postup), 6),
        round(float(c), 6),
        round(float(sd), 6),
        round(float(su), 6),
    )
    if label is not None:
        npar.label = label
    return npar


def nuispar_impacts(wkspace: Union[str, os.PathLike], sort: bool = True) -> List[NuisPar]:
    """Extract a list of nuisance parameter impacts from a fit.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of the TRExFitter workspace.

    Returns
    -------
    list(tdub.rex.NuisPar)
        The nuisance parameters.

    """
    nuispars = []
    np_ranking_yaml = yaml.full_load((PosixPath(wkspace) / "Ranking.yaml").read_text())
    for entry in np_ranking_yaml:
        nuispars.append(
            NuisPar(
                entry["Name"],
                entry["Name"],
                entry["POIdownPreFit"],
                entry["POIupPreFit"],
                entry["POIdown"],
                entry["POIup"],
                entry["NPhat"],
                entry["NPerrLo"],
                entry["NPerrHi"],
            )
        )
    if sort:
        return sorted(nuispars, key=lambda par: par.post_max)
    return nuispars


def nuispar_impact_plot_df(nuispars: List[NuisPar]) -> pd.DataFrame:
    """Construct a DataFrame to organize impact plot ingredients.

    Parameters
    ----------
    nuispars : list(NuisPar)
        The nuisance parameters.

    Returns
    -------
    pandas.DataFrame
        DataFrame describing the plot ingredients.

    """
    pre_down = np.array([p.pre_down for p in nuispars])
    pre_up = np.array([p.pre_up for p in nuispars])
    post_down = np.array([p.post_down for p in nuispars])
    post_up = np.array([p.post_up for p in nuispars])
    central = np.array([p.central for p in nuispars])
    sig_hi = np.array([p.sig_hi for p in nuispars])
    sig_lo = np.array([p.sig_lo for p in nuispars])
    pre_down_lefts = np.zeros_like(pre_down)
    pre_down_lefts[pre_down < 0] = pre_down[pre_down < 0]
    pre_up_lefts = np.zeros_like(pre_up)
    pre_up_lefts[pre_up < 0] = pre_up[pre_up < 0]
    post_down_lefts = np.zeros_like(post_down)
    post_down_lefts[post_down < 0] = post_down[post_down < 0]
    post_up_lefts = np.zeros_like(post_up)
    post_up_lefts[post_up < 0] = post_up[post_up < 0]
    ys = np.arange(len(pre_down))
    return pd.DataFrame.from_dict(
        dict(
            pre_down=pre_down,
            pre_up=pre_up,
            post_down=post_down,
            post_up=post_up,
            central=central,
            sig_hi=sig_hi,
            sig_lo=sig_lo,
            pre_down_lefts=pre_down_lefts,
            pre_up_lefts=pre_up_lefts,
            post_down_lefts=post_down_lefts,
            post_up_lefts=post_up_lefts,
            ys=ys,
        )
    )


def prettify_nuispar_label(label: str) -> str:
    """Fix nuisance parameter label to look nice for plots.

    Replace underscores with whitespace, TeXify some stuff, remove
    unnecessary things, etc.

    Parameters
    ----------
    label : str
        Original label.

    Returns
    -------
    str
        Prettified label.

    """
    return (
        label.replace("_", " ")
        .replace("ttbar", r"$t\bar{t}$")
        .replace("tW", r"$tW$")
        .replace("muF", r"$\mu_F$")
        .replace("muR", r"$\mu_R$")
        .replace("AR ", "")
        .replace("hdamp", r"$h_{\mathrm{damp}}$")
        .replace("DRDS", "DR vs DS")
        .replace("ptreweight", r"top-$p_{\mathrm{T}}$-reweight")
        .replace("MET", r"$E_{\mathrm{T}}^{\mathrm{miss}}$")
    )


def nuispar_impact_plot_top15(wkspace: Union[str, os.PathLike]) -> None:
    """Plot the top 15 nuisance parameters based on impact.

    Parameters
    ----------
    wkspace : str, os.PathLike
        Path of the TRExFitter workspace.

    """
    nuispars = nuispar_impacts(wkspace, sort=True)[-15:]
    for npar in nuispars:
        npar.label = prettify_nuispar_label(npar.label)
    df = nuispar_impact_plot_df(nuispars)
    ys = np.array(df.ys)
    # fmt: off
    fig, ax = plt.subplots(figsize=(5, 7.5))
    ax, ax2 = draw_impact_barh(ax, df)
    ax.legend(ncol=1, loc="upper left", bbox_to_anchor=(-0.75, 1.11))
    ax.set_xticks([-0.2, -0.1, 0.0, 0.1, 0.2])
    ax.set_ylim([-1, ys[-1] + 2.4])
    ax.set_yticklabels([p.label for p in nuispars])
    ax2.legend(loc="lower left", bbox_to_anchor=(-0.75, -0.09))
    ax2.set_xlabel(r"$\Delta\mu$", labelpad=25)
    ax.set_xlabel(r"$(\hat{\theta}-\theta_0)/\Delta\theta$", labelpad=20)
    ax.text(0.10, 0.95, "ATLAS", fontstyle="italic", fontweight="bold", size=14, transform=ax.transAxes)
    ax.text(0.37, 0.95, "Internal", size=14, transform=ax.transAxes)
    ax.text(0.10, 0.91, "$\\sqrt{s}$ = 13 TeV, $L = {139}$ fb$^{-1}$", size=12, transform=ax.transAxes)
    fig.subplots_adjust(left=0.45, bottom=0.085, top=0.915, right=0.975)
    mpl_dir = PosixPath(wkspace) / "matplotlib"
    mpl_dir.mkdir(exist_ok=True)
    output_file = str(mpl_dir / "Impact.pdf")
    fig.savefig(output_file)
    log.info("Created %s" % output_file)
    plt.close(fig)
    del fig, ax, ax2
    # fmt: on
    return 0


def _get_param(fit_file, name):
    with fit_file.open("r") as f:
        for line in f.readlines():
            if name in line:
                n, c, u, d = line.split()
                return n, float(c), float(u), float(d)


def delta_poi(
    wkspace1: Union[str, os.PathLike],
    wkspace2: Union[str, os.PathLike],
    fitname1: str = "tW",
    fitname2: str = "tW",
    poi: str = "SigXsecOverSM",
):
    r"""Calculate difference of a POI between two workspaces.

    The default arguments will perform a calculation of
    :math:`\Delta\mu` between two different fits. Standard error
    propagation is performed on both the up and down uncertainties.

    Parameters
    ----------
    wkspace1 : str or os.PathLike
        Path of the first TRExFitter workspace.
    wkspace2 : str or os.PathLike
        Path of the second TRExFitter workspace.
    fitname1 : str
        Name of the first fit.
    fitname2 : str
        Name of the second fit.
    poi : str
        Name of the parameter of interest.

    Returns
    -------
    :py:obj:`float`
        Central value of delta mu.
    :py:obj:`float`
        Up uncertainty on delta mu.
    :py:obj:`float`
        Down uncertainty on delta mu.

    """
    fit_file1 = PosixPath(wkspace1) / "Fits" / f"{fitname1}.txt"
    fit_file2 = PosixPath(wkspace2) / "Fits" / f"{fitname2}.txt"
    mu1 = _get_param(fit_file1, poi)
    mu2 = _get_param(fit_file2, poi)
    delta_mu = mu1[1] - mu2[1]
    sig_delta_mu_up = math.sqrt(mu1[2] ** 2 + mu2[2] ** 2)
    sig_delta_mu_dn = math.sqrt(mu1[3] ** 2 + mu2[3] ** 2)
    return delta_mu, sig_delta_mu_up, sig_delta_mu_dn


def compare_uncertainty(
    wkspace1: Union[str, os.PathLike],
    wkspace2: Union[str, os.PathLike],
    fitname1: str = "tW",
    fitname2: str = "tW",
    label1: Optional[str] = None,
    label2: Optional[str] = None,
    poi: str = "SigXsecOverSM",
    print_to: Optional[io.TextIOBase] = None,
) -> None:
    """Compare uncertainty between two fits.

    Parameters
    ----------
    wkspace1 : str or os.PathLike
        Path of the first TRExFitter workspace.
    wkspace2 : str or os.PathLike
        Path of the second TRExFitter workspace.
    fitname1 : str
        Name of the first fit.
    fitname2 : str
        Name of the second fit.
    label1 : str, optional
        Define label for the first fit (defaults to workspace path).
    label2 : str, optional
        Define label for the second fit (defaults to workspace path).
    poi : str
        Name of the parameter of interest.
    print_to : io.TextIOBase, optional
        Where to print results (defaults to sys.stdout).

    """
    if print_to is None:
        print_to = sys.stdout

    path1 = PosixPath(wkspace1).resolve()
    path2 = PosixPath(wkspace2).resolve()
    p1 = path1 if label1 is None else label1
    p2 = path2 if label2 is None else label2

    fit_file1 = path1 / "Fits" / f"{fitname1}.txt"
    fit_file2 = path2 / "Fits" / f"{fitname2}.txt"
    mu1 = _get_param(fit_file1, poi)
    mu2 = _get_param(fit_file2, poi)
    up1, down1 = mu1[2], mu1[3]
    up2, down2 = mu2[2], mu2[3]

    if abs(up1) > abs(up2):
        print(f"{p1} has a larger up uncertainty on {poi}", file=print_to)
        plarger = (abs(up1) - abs(up2)) / abs(up2) * 100.0
    else:
        print(f"{p2} has a larger up uncertainty on {poi}", file=print_to)
        plarger = (abs(up2) - abs(up1)) / abs(up1) * 100.0
    print(f"{p1}: {up1}", file=print_to)
    print(f"{p2}: {up2}", file=print_to)
    print(f"Percent larger: {plarger:3.4f}", file=print_to)

    print("----------------------------", file=print_to)

    if abs(down1) > abs(down2):
        print(f"{p1} has a larger down uncertainty on {poi}", file=print_to)
        plarger = (abs(down1) - abs(down2)) / abs(down2) * 100.0
    else:
        print(f"{p2} has a larger down uncertainty on {poi}", file=print_to)
        plarger = (abs(down2) - abs(down1)) / abs(down1) * 100.0
    print(f"{p1}: {down1}", file=print_to)
    print(f"{p2}: {down2}", file=print_to)
    print(f"Percent larger: {plarger:3.4f}", file=print_to)


def compare_nuispar(
    name: str,
    wkspace1: Union[str, os.PathLike],
    wkspace2: Union[str, os.PathLike],
    label1: Optional[str] = None,
    label2: Optional[str] = None,
    np_label: Optional[str] = None,
    print_to: Optional[io.TextIOBase] = None,
) -> None:
    """Compare nuisance parameter info between two fits.

    Parameters
    ----------
    name : str
        Name of the nuisance parameter.
    wkspace1 : str or os.PathLike
        Path of the first TRExFitter workspace.
    wkspace2 : str or os.PathLike
        Path of the second TRExFitter workspace.
    label1 : str, optional
        Define label for the first fit (defaults to workspace path).
    label2 : str, optional
        Define label for the second fit (defaults to workspace path).
    np_label : str, optional
        Give the nuisance parameter a label other than its name.
    print_to : io.TextIOBase, optional
        Where to print results (defaults to sys.stdout).

    """
    if print_to is None:
        print_to = sys.stdout

    path1 = PosixPath(wkspace1).resolve()
    path2 = PosixPath(wkspace2).resolve()
    p1 = path1 if label1 is None else label1
    p2 = path2 if label2 is None else label2
    np1 = nuispar_impact(wkspace1, name=name, label=np_label)
    np2 = nuispar_impact(wkspace2, name=name, label=np_label)

    print(f"{'=' * 15} Comparison for NP: {name} {'=' * 15}", file=print_to)

    if abs(np1.sig_lo) < abs(np2.sig_lo):
        print(f"{p1} has more aggressive sig lo {name} constraint", file=print_to)
        a, b = 1.0 - abs(np1.sig_lo), 1.0 - abs(np2.sig_lo)
    else:
        print(f"{p2} has more aggresive sig lo {name} constraint", file=print_to)
        b, a = 1.0 - abs(np1.sig_lo), 1.0 - abs(np2.sig_lo)
    plarger = (a - b) / b * 100.0
    print(f"{p1}: {np1.sig_lo}", file=print_to)
    print(f"{p2}: {np2.sig_lo}", file=print_to)
    print(f"Percent larger: {plarger:3.4f}", file=print_to)

    print("----------------------------", file=print_to)

    if abs(np1.sig_hi) < abs(np2.sig_hi):
        print(f"{p1} has a larger sig hi {name} constraint", file=print_to)
        a, b = 1.0 - abs(np1.sig_hi), 1.0 - abs(np2.sig_hi)
    else:
        print(f"{p2} has a larger sig hi {name} constraint", file=print_to)
        b, a = 1.0 - abs(np1.sig_hi), 1.0 - abs(np2.sig_hi)
    plarger = (a - b) / b * 100.0
    print(f"{p1}: {np1.sig_hi}", file=print_to)
    print(f"{p2}: {np2.sig_hi}", file=print_to)
    print(f"Percent larger: {plarger:3.4f}", file=print_to)

    if abs(np1.pre_up) > abs(np2.pre_up):
        print(f"{p1} has larger prefit up variation impact from {name}", file=print_to)
        plarger = (abs(np1.pre_up) - abs(np2.pre_up)) / abs(np2.pre_up) * 100.0
    else:
        print(f"{p2} has larger prefit up variation impact from {name}", file=print_to)
        plarger = (abs(np2.pre_up) - abs(np1.pre_up)) / abs(np1.pre_up) * 100.0
    print(f"{p1}: {np1.pre_up}", file=print_to)
    print(f"{p2}: {np2.pre_up}", file=print_to)
    print(f"Percent larger: {plarger:3.4f}", file=print_to)

    print("----------------------------", file=print_to)

    if abs(np1.pre_down) > abs(np2.pre_down):
        print(f"{p1} has larger prefit down variation impact from {name}", file=print_to)
        plarger = (abs(np1.pre_down) - abs(np2.pre_down)) / abs(np2.pre_down) * 100.0
    else:
        print(f"{p2} has larger prefit down variation impact from {name}", file=print_to)
        plarger = (abs(np2.pre_down) - abs(np1.pre_down)) / abs(np1.pre_down) * 100.0
    print(f"{p1}: {np1.pre_down}", file=print_to)
    print(f"{p2}: {np2.pre_down}", file=print_to)
    print(f"Percent larger: {plarger:3.4f}", file=print_to)

    print("----------------------------", file=print_to)

    if abs(np1.post_up) > abs(np2.post_up):
        print(f"{p1} has larger postfit up variation impact from {name}", file=print_to)
        plarger = (abs(np1.post_up) - abs(np2.post_up)) / abs(np2.post_up) * 100.0
    else:
        print(f"{p2} has larger postfit up variation impact from {name}", file=print_to)
        plarger = (abs(np2.post_up) - abs(np1.post_up)) / abs(np1.post_up) * 100.0
    print(f"{p1}: {np1.post_up}", file=print_to)
    print(f"{p2}: {np2.post_up}", file=print_to)
    print(f"Percent larger: {plarger:3.4f}", file=print_to)

    print("----------------------------", file=print_to)

    if abs(np1.post_down) > abs(np2.post_down):
        print(f"{p1} has larger postfit down variation impact from {name}", file=print_to)
        plarger = (abs(np1.post_down) - abs(np2.post_down)) / abs(np2.post_down) * 100.0
    else:
        print(f"{p2} has larger postfit down variation impact from {name}", file=print_to)
        plarger = (abs(np2.post_down) - abs(np1.post_down)) / abs(np1.post_down) * 100.0
    print(f"{p1}: {np1.post_down}", file=print_to)
    print(f"{p2}: {np2.post_down}", file=print_to)
    print(f"Percent larger: {plarger:3.4f}", file=print_to)


def comparison_summary(
    wkspace1,
    wkspace2,
    fitname1: str = "tW",
    fitname2: str = "tW",
    label1: Optional[str] = None,
    label2: Optional[str] = None,
    fit_poi: str = "SigXsecOverSM",
    nuispars: Optional[Iterable[str]] = None,
    nuispar_labels: Optional[Iterable[str]] = None,
    print_to: Optional[io.TextIOBase] = None,
) -> None:
    """Summarize a comparison of two fits.

    Parameters
    ----------
    wkspace1 : str or os.PathLike
        Path of the first TRExFitter workspace.
    wkspace2 : str or os.PathLike
        Path of the second TRExFitter workspace.
    fitname1 : str
        Name of the first fit.
    fitname2 : str
        Name of the second fit.
    label1 : str, optional
        Define label for the first fit (defaults to workspace path).
    label2 : str, optional
        Define label for the second fit (defaults to workspace path).
    fit_poi : str
        Name of the parameter of interest.
    nuispars : list(str), optional
        Nuisance parameters to compare.
    nuispar_labels: list(str), optional
        Labels to give each nuisance parameter other than the default
        name.
    print_to : io.TextIOBase, optional
        Where to print results (defaults to sys.stdout).

    """

    print(f"{'*' * 80}", file=print_to)
    print("Fit comparison summary", file=print_to)
    if label1 is not None and label2 is not None:
        print(f"Fit 1: {wkspace1} as {label1}", file=print_to)
        print(f"Fit 2: {wkspace2} as {label2}", file=print_to)
    print(f"{'-' * 60}", file=print_to)

    compare_uncertainty(
        wkspace1,
        wkspace2,
        fitname1=fitname1,
        fitname2=fitname2,
        label1=label1,
        label2=label2,
        poi=fit_poi,
        print_to=print_to,
    )
    if nuispars is not None:
        if nuispar_labels is not None:
            pairs = [(np, npl) for np, npl in zip(nuispars, nuispar_labels)]
        else:
            pairs = [(np, None) for np in nuispars]
        for np_name, np_label in pairs:
            compare_nuispar(
                np_name,
                wkspace1,
                wkspace2,
                label1=label1,
                label2=label2,
                np_label=np_label,
                print_to=print_to,
            )

    print(f"{'*' * 80}", file=print_to)
