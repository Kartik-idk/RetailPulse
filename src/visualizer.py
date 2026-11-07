"""
RetailPulse - Visualization Engine
Author: Kartikeya Pradhan
Subject: Python Programming (Semester 3)

This module builds a modern, dark-themed retail sales analytics dashboard
and standalone chart views using Matplotlib.
Consumes aggregated metrics exclusively from `data_processor.py`.
No third-party visualization frameworks (e.g. Seaborn, Plotly) are used.
"""

from typing import Any, Dict, List, Optional, Tuple

import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from src.data_processor import (
    calculate_kpis,
    get_branch_sales,
    get_category_gross_income,
    get_category_sales,
    get_customer_type_distribution,
    get_monthly_sales,
    get_payment_distribution,
    get_rating_analysis,
)


# -----------------------------------------------------------------------------
# Dark Theme Color Palette & Typography Constants
# -----------------------------------------------------------------------------
THEME = {
    # Backgrounds
    "main_bg": "#0B1120",        # Deep dark navy for master figure
    "panel_bg": "#131C2E",       # Balanced dark card/panel background
    "card_bg": "#1E293B",        # Secondary badge/accent container
    "border": "#23334D",         # Refined subtle card outline

    # Accents
    "primary": "#38BDF8",        # Electric sky blue (primary accent)
    "secondary": "#818CF8",      # Soft indigo/violet (secondary accent)
    "mint": "#34D399",           # Emerald/mint (positive income & success)
    "amber": "#FBBF24",          # Warm amber/gold (ratings & highlights)
    "coral": "#F472B6",          # Vibrant pink/coral (distinctions)
    "cyan": "#22D3EE",           # Vivid cyan

    # Typography
    "text_primary": "#F8FAFC",   # Bright white for titles and primary metrics
    "text_secondary": "#94A3B8", # Muted slate for axis labels and descriptions
    "text_muted": "#64748B",     # Dim slate for secondary footnotes
    "grid": "#1E293B",           # Subtle grid line color
}

# Distinct modern palette for multi-category charts
CATEGORY_PALETTE = [
    "#38BDF8",  # Electric Sky Blue
    "#60A5FA",  # Light Blue
    "#818CF8",  # Soft Indigo
    "#A78BFA",  # Lavender Purple
    "#C084FC",  # Violet
    "#E879F9",  # Orchid / Fuchsia
]


def apply_dark_theme(fig: plt.Figure, ax: plt.Axes, title: str = "") -> None:
    """
    Apply the consistent RetailPulse dark theme styling to a Matplotlib axis.

    Args:
        fig: The parent Figure object.
        ax: The target Axes object to style.
        title: Optional chart title string.
    """
    fig.patch.set_facecolor(THEME["main_bg"])
    ax.set_facecolor(THEME["panel_bg"])

    # Spine styling
    for spine in ax.spines.values():
        spine.set_color(THEME["border"])
        spine.set_linewidth(1.0)

    # Tick and label styling
    ax.tick_params(colors=THEME["text_secondary"], labelsize=8.5, which="both", length=3.5)
    ax.xaxis.label.set_color(THEME["text_secondary"])
    ax.yaxis.label.set_color(THEME["text_secondary"])
    ax.xaxis.label.set_size(9)
    ax.yaxis.label.set_size(9)

    # Grid styling
    ax.grid(True, color=THEME["grid"], linestyle="--", linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)

    # Title styling
    if title:
        ax.set_title(
            title,
            color=THEME["text_primary"],
            fontsize=10.5,
            fontweight="bold",
            pad=11,
        )


def _set_window_title(fig: plt.Figure, title: str) -> None:
    """Set window title if GUI canvas manager is available."""
    if hasattr(fig.canvas, "manager") and fig.canvas.manager is not None:
        try:
            fig.canvas.manager.set_window_title(f"RetailPulse - {title}")
        except Exception:
            pass


def _draw_empty_placeholder(ax: plt.Axes, message: str = "No Data Available") -> None:
    """Display a centered fallback message on an empty axis."""
    ax.text(
        0.5,
        0.5,
        message,
        color=THEME["text_secondary"],
        fontsize=11,
        ha="center",
        va="center",
        transform=ax.transAxes,
    )
    ax.set_xticks([])
    ax.set_yticks([])


# -----------------------------------------------------------------------------
# Individual Chart Functions
# -----------------------------------------------------------------------------

def plot_monthly_revenue_trend(
    records: List[Dict[str, Any]],
    ax: Optional[plt.Axes] = None,
    show: bool = True,
    save_path: Optional[str] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot the monthly revenue trend line chart with chronological ordering.

    Args:
        records: List of transactional records.
        ax: Optional existing Axes to render on.
        show: If True and ax is None, call plt.show().
        save_path: Optional path to save the generated figure.

    Returns:
        Tuple[plt.Figure, plt.Axes]: The figure and axes instances.
    """
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    else:
        fig = ax.figure

    apply_dark_theme(fig, ax, title="Monthly Revenue Trend")

    monthly_data = get_monthly_sales(records)
    if not monthly_data:
        _draw_empty_placeholder(ax, "No Monthly Data Available")
        return fig, ax

    labels = [info["label"] for info in monthly_data.values()]
    revenues = [info["revenue"] for info in monthly_data.values()]
    x_indices = list(range(len(labels)))

    # Main trend line with distinct halo markers
    ax.plot(
        x_indices,
        revenues,
        color=THEME["primary"],
        linewidth=2.8,
        marker="o",
        markersize=7.5,
        markerfacecolor=THEME["main_bg"],
        markeredgecolor=THEME["primary"],
        markeredgewidth=2.2,
        label="Revenue",
        zorder=4,
    )

    # Soft area fill underneath
    ax.fill_between(x_indices, revenues, color=THEME["primary"], alpha=0.15, zorder=3)

    # Format Axes with margin padding so endpoints and labels do not collide with spines
    ax.set_xticks(x_indices)
    ax.set_xticklabels(labels, color=THEME["text_primary"], fontweight="normal", fontsize=8.5)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"${val*1e-3:.0f}K"))

    # Horizontal boundary padding
    ax.set_xlim(-0.35, len(labels) - 1 + 0.35)

    # Vertical margin for data labels and breathing room
    min_rev, max_rev = min(revenues), max(revenues)
    y_span = max_rev - min_rev if max_rev > min_rev else 5000
    ax.set_ylim(max(0, min_rev - y_span * 0.45), max_rev + y_span * 0.40)

    # Value callout labels on data points positioned cleanly above markers
    for idx, rev in enumerate(revenues):
        ax.annotate(
            f"${rev:,.0f}",
            (idx, rev),
            textcoords="offset points",
            xytext=(0, 11),
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color=THEME["text_primary"],
            bbox=dict(
                boxstyle="round,pad=0.25",
                facecolor=THEME["card_bg"],
                edgecolor=THEME["border"],
                alpha=0.95,
            ),
            zorder=5,
        )

    if standalone:
        _set_window_title(fig, "Monthly Revenue Trend")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, facecolor=THEME["main_bg"], bbox_inches="tight")
        if show:
            plt.show()
            plt.close(fig)

    return fig, ax


def plot_revenue_by_category(
    records: List[Dict[str, Any]],
    ax: Optional[plt.Axes] = None,
    show: bool = True,
    save_path: Optional[str] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot horizontal bar chart ranking revenue by Product line.

    Args:
        records: List of transactional records.
        ax: Optional existing Axes to render on.
        show: If True and ax is None, call plt.show().
        save_path: Optional path to save the generated figure.

    Returns:
        Tuple[plt.Figure, plt.Axes]: The figure and axes instances.
    """
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    else:
        fig = ax.figure

    apply_dark_theme(fig, ax, title="Revenue by Product Category")

    category_sales = get_category_sales(records, sort_descending=True)
    if not category_sales:
        _draw_empty_placeholder(ax, "No Category Data Available")
        return fig, ax

    # Invert so highest appears at the top
    categories = list(category_sales.keys())[::-1]
    revenues = [category_sales[c] for c in categories]
    # Gradient palette aligned so top revenue bar gets the primary electric accent
    colors = CATEGORY_PALETTE[::-1][: len(categories)]

    y_pos = list(range(len(categories)))
    bars = ax.barh(
        y_pos,
        revenues,
        height=0.52,
        color=colors,
        edgecolor=THEME["border"],
        linewidth=0.8,
        zorder=3,
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, color=THEME["text_primary"], fontsize=8.5)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"${val*1e-3:.0f}K"))
    ax.set_xlim(0, max(revenues) * 1.18)

    # Value labels at end of bars
    for bar, val in zip(bars, revenues):
        width = bar.get_width()
        ax.text(
            width + (max(revenues) * 0.02),
            bar.get_y() + bar.get_height() / 2,
            f"${val:,.0f}",
            va="center",
            ha="left",
            color=THEME["text_primary"],
            fontsize=8.5,
            fontweight="bold",
        )

    if standalone:
        _set_window_title(fig, "Revenue by Product Category")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, facecolor=THEME["main_bg"], bbox_inches="tight")
        if show:
            plt.show()
            plt.close(fig)

    return fig, ax


def plot_branch_performance(
    records: List[Dict[str, Any]],
    ax: Optional[plt.Axes] = None,
    show: bool = True,
    save_path: Optional[str] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot bar chart comparing revenue and volume across supermarket branches.

    Args:
        records: List of transactional records.
        ax: Optional existing Axes to render on.
        show: If True and ax is None, call plt.show().
        save_path: Optional path to save the generated figure.

    Returns:
        Tuple[plt.Figure, plt.Axes]: The figure and axes instances.
    """
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    else:
        fig = ax.figure

    apply_dark_theme(fig, ax, title="Branch Performance & Revenue")

    branches = get_branch_sales(records)
    if not branches:
        _draw_empty_placeholder(ax, "No Branch Data Available")
        return fig, ax

    branch_names = list(branches.keys())
    labels = [f"Branch {b}\n({branches[b]['city']})" for b in branch_names]
    revenues = [branches[b]["revenue"] for b in branch_names]
    transactions = [branches[b]["transactions"] for b in branch_names]
    ratings = [branches[b]["average_rating"] for b in branch_names]

    branch_colors = [THEME["primary"], THEME["secondary"], THEME["mint"]]
    x_pos = list(range(len(labels)))

    bars = ax.bar(
        x_pos,
        revenues,
        width=0.46,
        color=branch_colors[: len(branch_names)],
        edgecolor=THEME["border"],
        linewidth=0.8,
        zorder=3,
    )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, color=THEME["text_primary"], fontsize=8.5)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"${val*1e-3:.0f}K"))
    ax.set_ylim(0, max(revenues) * 1.22)

    # Value labels and high-contrast metadata badges inside bars
    for bar, val, tx, rat in zip(bars, revenues, transactions, ratings):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + (max(revenues) * 0.02),
            f"${val:,.0f}",
            ha="center",
            va="bottom",
            color=THEME["text_primary"],
            fontsize=8.5,
            fontweight="bold",
        )
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height * 0.52,
            f"{tx} txns\n★ {rat:.2f}",
            ha="center",
            va="center",
            color=THEME["text_primary"],
            fontsize=8,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor=THEME["main_bg"],
                edgecolor=THEME["border"],
                alpha=0.65,
                linewidth=0.6,
            ),
            zorder=4,
        )

    if standalone:
        _set_window_title(fig, "Branch Performance & Revenue")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, facecolor=THEME["main_bg"], bbox_inches="tight")
        if show:
            plt.show()
            plt.close(fig)

    return fig, ax


def plot_payment_distribution(
    records: List[Dict[str, Any]],
    ax: Optional[plt.Axes] = None,
    show: bool = True,
    save_path: Optional[str] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot modern donut chart representing payment method distribution.

    Args:
        records: List of transactional records.
        ax: Optional existing Axes to render on.
        show: If True and ax is None, call plt.show().
        save_path: Optional path to save the generated figure.

    Returns:
        Tuple[plt.Figure, plt.Axes]: The figure and axes instances.
    """
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
    else:
        fig = ax.figure

    apply_dark_theme(fig, ax, title="Payment Method Distribution")
    ax.grid(False)

    payments = get_payment_distribution(records)
    if not payments:
        _draw_empty_placeholder(ax, "No Payment Data Available")
        return fig, ax

    methods = list(payments.keys())
    counts = [payments[m]["count"] for m in methods]
    colors = [THEME["primary"], THEME["secondary"], THEME["amber"]]

    wedges, texts, autotexts = ax.pie(
        counts,
        labels=None,
        autopct="%1.1f%%",
        pctdistance=0.75,
        startangle=140,
        colors=colors[: len(methods)],
        wedgeprops=dict(width=0.38, edgecolor=THEME["panel_bg"], linewidth=2.5),
    )

    for autotext in autotexts:
        autotext.set_color(THEME["text_primary"])
        autotext.set_fontsize(8.5)
        autotext.set_weight("bold")

    # Center label in donut hole
    total_tx = sum(counts)
    ax.text(
        0,
        0.05,
        f"{total_tx:,}",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=THEME["text_primary"],
    )
    ax.text(
        0,
        -0.18,
        "Payments",
        ha="center",
        va="center",
        fontsize=8,
        color=THEME["text_secondary"],
    )

    # Compact legend formatted cleanly within subplot bounds
    legend_labels = [
        f"{m}: {payments[m]['count']} (${payments[m]['revenue']*1e-3:.0f}K)"
        for m in methods
    ]
    ax.legend(
        wedges,
        legend_labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=len(methods),
        frameon=False,
        fontsize=7.8,
        labelcolor=THEME["text_secondary"],
        handletextpad=0.3,
        columnspacing=0.8,
    )

    if standalone:
        _set_window_title(fig, "Payment Method Distribution")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, facecolor=THEME["main_bg"], bbox_inches="tight")
        if show:
            plt.show()
            plt.close(fig)

    return fig, ax


def plot_customer_type_distribution(
    records: List[Dict[str, Any]],
    ax: Optional[plt.Axes] = None,
    show: bool = True,
    save_path: Optional[str] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot donut chart comparing Member vs Normal customer transaction proportions.

    Args:
        records: List of transactional records.
        ax: Optional existing Axes to render on.
        show: If True and ax is None, call plt.show().
        save_path: Optional path to save the generated figure.

    Returns:
        Tuple[plt.Figure, plt.Axes]: The figure and axes instances.
    """
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
    else:
        fig = ax.figure

    apply_dark_theme(fig, ax, title="Customer Type Distribution")
    ax.grid(False)

    customers = get_customer_type_distribution(records)
    if not customers:
        _draw_empty_placeholder(ax, "No Customer Data Available")
        return fig, ax

    types = list(customers.keys())
    counts = [customers[t]["count"] for t in types]
    colors = [THEME["primary"], THEME["mint"]]

    wedges, texts, autotexts = ax.pie(
        counts,
        labels=None,
        autopct="%1.1f%%",
        pctdistance=0.74,
        startangle=90,
        colors=colors[: len(types)],
        wedgeprops=dict(width=0.38, edgecolor=THEME["panel_bg"], linewidth=2.5),
    )

    for autotext in autotexts:
        autotext.set_color(THEME["text_primary"])
        autotext.set_fontsize(8.5)
        autotext.set_weight("bold")

    # Center label in donut hole
    total_tx = sum(counts)
    ax.text(
        0,
        0.05,
        f"{total_tx:,}",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=THEME["text_primary"],
    )
    ax.text(
        0,
        -0.18,
        "Shoppers",
        ha="center",
        va="center",
        fontsize=8,
        color=THEME["text_secondary"],
    )

    legend_labels = [
        f"{t}: {customers[t]['count']} txns (${customers[t]['revenue']*1e-3:.1f}K)"
        for t in types
    ]
    ax.legend(
        wedges,
        legend_labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=len(types),
        frameon=False,
        fontsize=7.8,
        labelcolor=THEME["text_secondary"],
        handletextpad=0.4,
        columnspacing=1.0,
    )

    if standalone:
        _set_window_title(fig, "Customer Type Distribution")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, facecolor=THEME["main_bg"], bbox_inches="tight")
        if show:
            plt.show()
            plt.close(fig)

    return fig, ax


def plot_gross_income_by_category(
    records: List[Dict[str, Any]],
    ax: Optional[plt.Axes] = None,
    show: bool = True,
    save_path: Optional[str] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot bar chart comparing total gross income across product categories.

    Args:
        records: List of transactional records.
        ax: Optional existing Axes to render on.
        show: If True and ax is None, call plt.show().
        save_path: Optional path to save the generated figure.

    Returns:
        Tuple[plt.Figure, plt.Axes]: The figure and axes instances.
    """
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    else:
        fig = ax.figure

    apply_dark_theme(fig, ax, title="Gross Income by Category")

    income_data = get_category_gross_income(records, sort_descending=True)
    if not income_data:
        _draw_empty_placeholder(ax, "No Gross Income Data Available")
        return fig, ax

    categories = list(income_data.keys())
    incomes = [income_data[c] for c in categories]
    # Clean two-line title-cased labels for horizontal presentation without cramped rotation
    display_labels = [
        c.title().replace(" And ", " &\n")
        if " and " in c.lower()
        else c.title().replace(" ", "\n", 1)
        for c in categories
    ]

    x_pos = list(range(len(categories)))
    bars = ax.bar(
        x_pos,
        incomes,
        width=0.52,
        color=THEME["mint"],
        edgecolor=THEME["border"],
        linewidth=0.8,
        zorder=3,
    )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(display_labels, color=THEME["text_primary"], fontsize=8, rotation=0, ha="center")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"${val*1e-3:.1f}K"))
    ax.set_ylim(0, max(incomes) * 1.20)

    for bar, val in zip(bars, incomes):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + (max(incomes) * 0.02),
            f"${val:,.0f}",
            ha="center",
            va="bottom",
            color=THEME["text_primary"],
            fontsize=8.5,
            fontweight="bold",
        )

    if standalone:
        _set_window_title(fig, "Gross Income by Category")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, facecolor=THEME["main_bg"], bbox_inches="tight")
        if show:
            plt.show()
            plt.close(fig)

    return fig, ax


def plot_rating_analysis(
    records: List[Dict[str, Any]],
    ax: Optional[plt.Axes] = None,
    show: bool = True,
    save_path: Optional[str] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot customer satisfaction rating breakdown across product categories.

    Args:
        records: List of transactional records.
        ax: Optional existing Axes to render on.
        show: If True and ax is None, call plt.show().
        save_path: Optional path to save the generated figure.

    Returns:
        Tuple[plt.Figure, plt.Axes]: The figure and axes instances.
    """
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    else:
        fig = ax.figure

    apply_dark_theme(fig, ax, title="Customer Rating by Product Category")

    rating_info = get_rating_analysis(records)
    by_category = rating_info.get("by_category", {})
    if not by_category:
        _draw_empty_placeholder(ax, "No Rating Data Available")
        return fig, ax

    categories = list(by_category.keys())[::-1]
    avg_ratings = [by_category[c]["average_rating"] for c in categories]
    overall_avg = rating_info.get("overall_average", 6.97)

    y_pos = list(range(len(categories)))
    bars = ax.barh(
        y_pos,
        avg_ratings,
        height=0.55,
        color=THEME["amber"],
        edgecolor=THEME["border"],
        linewidth=0.8,
        zorder=3,
    )

    # Benchmark reference line for overall average
    ax.axvline(
        overall_avg,
        color=THEME["primary"],
        linestyle="--",
        linewidth=1.2,
        alpha=0.9,
        label=f"Overall Avg ({overall_avg} ★)",
        zorder=4,
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, color=THEME["text_primary"], fontsize=8.5)
    ax.set_xlim(0, 10.5)

    for bar, val in zip(bars, avg_ratings):
        width = bar.get_width()
        ax.text(
            width + 0.15,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f} ★",
            va="center",
            ha="left",
            color=THEME["text_primary"],
            fontsize=8,
            fontweight="bold",
        )

    ax.legend(loc="lower right", frameon=False, fontsize=8, labelcolor=THEME["text_secondary"])

    if standalone:
        _set_window_title(fig, "Customer Rating Analysis")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, facecolor=THEME["main_bg"], bbox_inches="tight")
        if show:
            plt.show()
            plt.close(fig)

    return fig, ax


# -----------------------------------------------------------------------------
# Complete Master Dashboard
# -----------------------------------------------------------------------------

def _render_kpi_card(
    ax: plt.Axes,
    label: str,
    value: str,
    accent_color: str,
    subtitle: str = "",
) -> None:
    """Draw a modern rounded KPI metric card into a dedicated axis."""
    ax.set_facecolor(THEME["main_bg"])
    ax.axis("off")

    # Card background container patch
    card_patch = FancyBboxPatch(
        (0.02, 0.04),
        0.96,
        0.92,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        facecolor=THEME["panel_bg"],
        edgecolor=THEME["border"],
        linewidth=1.1,
        transform=ax.transAxes,
        zorder=1,
    )
    ax.add_patch(card_patch)

    # Top accent bar spanning gracefully across the card top
    accent_bar = FancyBboxPatch(
        (0.15, 0.88),
        0.70,
        0.04,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=accent_color,
        edgecolor="none",
        transform=ax.transAxes,
        zorder=2,
    )
    ax.add_patch(accent_bar)

    # Card title / label (centered)
    ax.text(
        0.50,
        0.70,
        label.upper(),
        color=THEME["text_secondary"],
        fontsize=8,
        fontweight="bold",
        ha="center",
        va="center",
        transform=ax.transAxes,
        zorder=3,
    )

    # Main metric value (centered)
    ax.text(
        0.50,
        0.42,
        value,
        color=accent_color,
        fontsize=15,
        fontweight="bold",
        ha="center",
        va="center",
        transform=ax.transAxes,
        zorder=3,
    )

    # Subtitle or supplementary info (centered)
    if subtitle:
        ax.text(
            0.50,
            0.18,
            subtitle,
            color=THEME["text_muted"],
            fontsize=7.5,
            ha="center",
            va="center",
            transform=ax.transAxes,
            zorder=3,
        )


def render_complete_dashboard(
    records: List[Dict[str, Any]],
    save_path: Optional[str] = None,
    show: bool = True,
) -> plt.Figure:
    """
    Generate and render the complete executive retail sales analytics dashboard.

    Layout Structure:
        - Header: Title, subtitle, dataset period, and transaction counter
        - KPI Banner: 5 distinct metric cards (Revenue, Txns, Units, AOV, Rating)
        - Subplot Grid (2x3):
            1. Monthly Revenue Trend (Line)
            2. Revenue by Product Category (Horizontal Bar)
            3. Payment Method Distribution (Donut)
            4. Branch Performance (Bar)
            5. Customer Type Distribution (Donut)
            6. Gross Income by Category (Bar)

    Args:
        records: List of cleaned transactional record dictionaries.
        save_path: Optional file path to export the dashboard image.
        show: If True, display the window using plt.show().

    Returns:
        plt.Figure: The master figure object.
    """
    # Create master figure with high resolution
    fig = plt.figure(figsize=(18, 12), dpi=100, facecolor=THEME["main_bg"])

    # Configure top-level GridSpec with balanced proportions
    # Rows: 0=Header (0.28), 1=KPI Cards (0.50), 2=Chart Row 1 (1.38), 3=Chart Row 2 (1.38)
    main_gs = gridspec.GridSpec(
        4,
        1,
        figure=fig,
        height_ratios=[0.28, 0.50, 1.38, 1.38],
        top=0.965,
        bottom=0.060,
        left=0.045,
        right=0.955,
        hspace=0.34,
    )

    # -------------------------------------------------------------------------
    # 1. Header Section
    # -------------------------------------------------------------------------
    header_ax = fig.add_subplot(main_gs[0])
    header_ax.set_facecolor(THEME["main_bg"])
    header_ax.axis("off")

    # Title & Subtitle
    header_ax.text(
        0.0,
        0.66,
        "RETAILPULSE",
        color=THEME["primary"],
        fontsize=20,
        fontweight="bold",
        va="center",
        transform=header_ax.transAxes,
    )
    header_ax.text(
        0.135,
        0.66,
        "|   Executive Retail Sales Analytics Dashboard",
        color=THEME["text_primary"],
        fontsize=13,
        fontweight="normal",
        va="center",
        transform=header_ax.transAxes,
    )
    header_ax.text(
        0.0,
        0.18,
        "Dataset Horizon: January 01, 2019 – March 30, 2019    •    Core Python Analytics Engine    •    Matplotlib Visualizer",
        color=THEME["text_secondary"],
        fontsize=8.5,
        va="center",
        transform=header_ax.transAxes,
    )

    # Status Pill on the right
    tx_count = len(records)
    header_ax.text(
        1.0,
        0.50,
        f"● ACTIVE DATASET: {tx_count:,} TRANSACTIONS",
        color=THEME["mint"],
        fontsize=8.5,
        fontweight="bold",
        ha="right",
        va="center",
        transform=header_ax.transAxes,
        bbox=dict(
            boxstyle="round,pad=0.4,rounding_size=0.4",
            facecolor=THEME["panel_bg"],
            edgecolor=THEME["border"],
            alpha=0.95,
        ),
    )

    # -------------------------------------------------------------------------
    # 2. KPI Section (5 Cards)
    # -------------------------------------------------------------------------
    kpis = calculate_kpis(records)
    kpi_gs = gridspec.GridSpecFromSubplotSpec(1, 5, subplot_spec=main_gs[1], wspace=0.14)

    kpi_configs = [
        ("Total Revenue", f"${kpis['total_revenue']:,.2f}", THEME["primary"], "Across 3 months"),
        ("Transactions", f"{kpis['total_transactions']:,}", THEME["secondary"], "Verified orders"),
        ("Units Sold", f"{kpis['total_units_sold']:,}", THEME["mint"], "Total quantity"),
        ("Avg Order Value", f"${kpis['average_order_value']:,.2f}", THEME["cyan"], "Per transaction"),
        ("Avg Rating", f"{kpis['average_rating']:.2f} ★", THEME["amber"], "Out of 10.0 scale"),
    ]

    for idx, (label, val, color, sub) in enumerate(kpi_configs):
        ax_card = fig.add_subplot(kpi_gs[0, idx])
        _render_kpi_card(ax_card, label, val, color, sub)

    # -------------------------------------------------------------------------
    # 3. Chart Grid Rows (2 rows x 3 columns)
    # -------------------------------------------------------------------------
    charts_r1 = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=main_gs[2], wspace=0.24)
    charts_r2 = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=main_gs[3], wspace=0.24)

    # Row 1 Charts
    ax1 = fig.add_subplot(charts_r1[0, 0])
    plot_monthly_revenue_trend(records, ax=ax1, show=False)

    ax2 = fig.add_subplot(charts_r1[0, 1])
    plot_revenue_by_category(records, ax=ax2, show=False)

    ax3 = fig.add_subplot(charts_r1[0, 2])
    plot_payment_distribution(records, ax=ax3, show=False)

    # Row 2 Charts
    ax4 = fig.add_subplot(charts_r2[0, 0])
    plot_branch_performance(records, ax=ax4, show=False)

    ax5 = fig.add_subplot(charts_r2[0, 1])
    plot_customer_type_distribution(records, ax=ax5, show=False)

    ax6 = fig.add_subplot(charts_r2[0, 2])
    plot_gross_income_by_category(records, ax=ax6, show=False)

    _set_window_title(fig, "Executive Sales Analytics Dashboard")

    # Export figure if save path is provided
    if save_path:
        fig.savefig(save_path, facecolor=THEME["main_bg"], edgecolor="none", dpi=120)

    # Interactive display
    if show:
        plt.show()
        plt.close(fig)

    return fig
