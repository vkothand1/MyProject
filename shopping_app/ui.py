from __future__ import annotations

import uuid
from datetime import datetime

import streamlit as st

from shopping_app.config import get_settings
from shopping_app.db import ShoppingRepository
from shopping_app.graph.workflow import ShoppingGraphService

st.set_page_config(
    page_title="My Shopping Recommender",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Marketplace logos (public CDN favicons / brand images)
# ---------------------------------------------------------------------------
_PLATFORM_LOGO: dict[str, str] = {
    "amazon": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
    "walmart": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Walmart_logo.svg",
    "costco": "https://upload.wikimedia.org/wikipedia/commons/5/59/Costco_Wholesale_logo_2010-10-26.svg",
    "target": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Target_logo.svg",
}

# ---------------------------------------------------------------------------
# Custom CSS for a polished, animated look
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- global ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* gradient header banner */
    .brand-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        animation: slideDown 0.6s ease-out;
    }
    .brand-header h1 {
        color: #fff;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .brand-header p {
        color: rgba(255,255,255,0.85);
        margin: 0.25rem 0 0 0;
        font-size: 0.95rem;
    }

    /* slide-down */
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    /* fade-in */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* product cards */
    .product-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
        border: 1px solid #e2e6f0;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        animation: fadeIn 0.5s ease-out;
    }
    .product-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.18);
    }

    /* price tag */
    .price-tag {
        display: inline-block;
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: #fff;
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 0.4rem 0;
    }

    /* platform badge with logo */
    .platform-logo-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #f0f2f6;
        border: 1px solid #ddd;
        padding: 0.25rem 0.65rem;
        border-radius: 10px;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #333;
        vertical-align: middle;
    }
    .platform-logo-badge img {
        height: 18px;
        width: auto;
        object-fit: contain;
    }

    /* status badge */
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-recommended { background: #e3f2fd; color: #1565c0; }
    .status-selected    { background: #e8f5e9; color: #2e7d32; }
    .status-added       { background: #f3e5f5; color: #7b1fa2; }

    /* sidebar polish */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #38ef7d !important;
        font-size: 0.82rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        font-size: 0.72rem !important;
    }

    /* section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.5rem 0 1rem 0;
        animation: fadeIn 0.4s ease-out;
    }
    .section-header h2 {
        margin: 0;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #999;
        animation: fadeIn 0.6s ease-out;
    }
    .empty-state .icon { font-size: 3rem; margin-bottom: 0.5rem; }

    /* pulse animation for AI spinner */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0.5; }
    }
    .ai-working { animation: pulse 1.5s ease-in-out infinite; }

    /* price verified badge */
    .price-verified {
        display: inline-block;
        background: #e8f5e9;
        color: #2e7d32;
        padding: 0.15rem 0.5rem;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 0.4rem;
    }
    .price-estimated {
        display: inline-block;
        background: #fff3e0;
        color: #e65100;
        padding: 0.15rem 0.5rem;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_service() -> ShoppingGraphService:
    return ShoppingGraphService()


def init_state() -> None:
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "page" not in st.session_state:
        st.session_state.page = "Find Items"
    if "pending_purge" not in st.session_state:
        st.session_state.pending_purge = False
    if "pending_purge_count" not in st.session_state:
        st.session_state.pending_purge_count = 0
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""


def brand_header() -> None:
    st.markdown(
        """
        <div class="brand-header">
            <h1>🛍️ My Shopping Recommender</h1>
            <p>AI-powered product discovery across Amazon, Walmart, Costco & Target</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar() -> None:
    settings = get_settings()
    with st.sidebar:
        st.markdown("### 🛍️ My Shopping Recommender")
        st.caption("AI-powered • Human-approved")
        st.divider()
        st.text(f"🔑 Session: {st.session_state.session_id[:8]}")
        st.radio(
            "Navigate",
            ["Find Items", "Cart Review", "Added To Platform", "History Purge", "Settings"],
            key="page",
        )
        st.divider()
        st.markdown(
            f'<p style="font-size:0.75rem;color:#aaa;margin:0;">📍 Shipping ZIP</p>'
            f'<p style="font-size:0.85rem;color:#38ef7d;margin:0 0 0.6rem 0;font-weight:600;">'
            f'{settings.shipping_zip}</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p style="font-size:0.75rem;color:#aaa;margin:0;">🏪 Platforms</p>'
            f'<p style="font-size:0.85rem;color:#38ef7d;margin:0;font-weight:600;">'
            f'{", ".join(p.title() for p in settings.allowed_platforms)}</p>',
            unsafe_allow_html=True,
        )
        st.caption("Brand-new, in-stock products only.")


def _platform_logo_badge(platform: str) -> str:
    logo = _PLATFORM_LOGO.get(platform.lower(), "")
    img_tag = f'<img src="{logo}" alt="{platform}">' if logo else ""
    return f'<span class="platform-logo-badge">{img_tag}{platform.title()}</span>'


def _status_badge(status: str) -> str:
    css_class = {
        "recommended": "status-recommended",
        "selected": "status-selected",
        "added_to_platform": "status-added",
    }.get(status, "status-recommended")
    label = status.replace("_", " ").title()
    return f'<span class="status-badge {css_class}">{label}</span>'


def _price_badge(row: dict) -> str:
    if row.get("price_verified"):
        return '<span class="price-verified">✓ Price verified</span>'
    return '<span class="price-estimated">~ Estimated price</span>'


# ---------- Find Items ----------

def render_find_items(service: ShoppingGraphService, repo: ShoppingRepository) -> None:
    st.markdown(
        '<div class="section-header"><h2>🔍 Find Items</h2></div>',
        unsafe_allow_html=True,
    )
    st.write(
        "Describe what you're looking for. The AI Recommender Agent will discover "
        "brand-new, in-stock products across Amazon, Walmart, Costco & Target, "
        "then rank the best match by relevance and total cost."
    )
    query = st.text_area("What are you looking for?", value=st.session_state.last_query, height=100)
    if st.button("🤖 Recommender AI Agent", type="primary", use_container_width=False):
        if not query.strip():
            st.error("Please enter an item description.")
            return
        st.session_state.last_query = query
        with st.spinner("🤖 AI Agent is searching marketplaces and ranking…"):
            result = service.recommend(query=query, session_id=st.session_state.session_id)
        st.success(result.get("message", "Recommendations ready."))

    recommendations = repo.list_recommendations(st.session_state.session_id)
    if not recommendations:
        st.markdown(
            '<div class="empty-state"><div class="icon">🔎</div>'
            "No recommendations yet. Describe an item above and run the AI agent.</div>",
            unsafe_allow_html=True,
        )
        return

    for row in recommendations:
        _render_recommendation_card(row, repo)


def _render_recommendation_card(row: dict, repo: ShoppingRepository) -> None:
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(
            f'{_platform_logo_badge(row["platform"])} '
            f'{_status_badge(row["status"])}',
            unsafe_allow_html=True,
        )
        st.markdown(f"### {row['title']}")
        st.markdown(
            f'<span class="price-tag">${row["total_cost"]:.2f} total</span>'
            f'{_price_badge(row)}',
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        c1.metric("Item price", f"${row['item_price']:.2f}")
        c2.metric("Shipping", f"${row['shipping_cost']:.2f}")
        st.markdown(f"📅 Listed: {row['list_date']}")
        if row.get("platform_added_date"):
            st.markdown(f"✅ Added to platform: {row['platform_added_date']}")
        st.markdown(f"[🔗 Open item link]({row['url']})")
        if row.get("notes"):
            st.caption(f"💡 {row['notes']}")
    with col2:
        if st.button("🤖 Product Selector Agent", key=f"select_{row['id']}", use_container_width=True):
            repo.select_item(int(row["id"]))
            st.toast(f"✅ '{row['title']}' selected by Product Selector Agent.")
            st.rerun()
        if st.button("❌ Reject", key=f"reject_{row['id']}", use_container_width=True):
            repo.reject_item(int(row["id"]))
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- Cart Review ----------

def render_cart_review(service: ShoppingGraphService, repo: ShoppingRepository) -> None:
    st.markdown(
        '<div class="section-header"><h2>🛒 Cart Review</h2></div>',
        unsafe_allow_html=True,
    )
    st.write(
        "1. Click **Open on marketplace** to view the product page and add it to your real cart.\n"
        "2. Once added, click **Mark as Added** to record it in your history."
    )
    active = repo.list_active_items(st.session_state.session_id)
    if not active:
        st.markdown(
            '<div class="empty-state"><div class="icon">🛒</div>'
            "No items to review. Use <b>Find Items</b> to get a recommendation first.</div>",
            unsafe_allow_html=True,
        )
        return

    for row in active:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(
                f'{_platform_logo_badge(row["platform"])} '
                f'{_status_badge(row["status"])}',
                unsafe_allow_html=True,
            )
            st.markdown(f"### {row['title']}")
            st.markdown(
                f'<span class="price-tag">${row["total_cost"]:.2f} total</span>'
                f'{_price_badge(row)}',
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            c1.metric("Item price", f"${row['item_price']:.2f}")
            c2.metric("Shipping", f"${row['shipping_cost']:.2f}")
            if row.get("notes"):
                st.caption(f"💡 {row['notes']}")
        with col2:
            # Step 1: open the marketplace product page
            st.link_button(
                f"🔗 Open on {row['platform'].title()}",
                row["url"],
                use_container_width=True,
            )
            # Step 2: after user adds on marketplace, record it locally
            if st.button("✅ Mark as Added", key=f"add_cart_{row['id']}", type="primary", use_container_width=True):
                # Open the product page in a new tab via JS, then mark locally
                st.markdown(
                    f'<script>window.open("{row["url"]}", "_blank");</script>',
                    unsafe_allow_html=True,
                )
                service.add_single_item(st.session_state.session_id, int(row["id"]))
                st.toast(f"✅ '{row['title']}' marked as added to {row['platform'].title()} cart. The product page has been opened — please add it to your marketplace cart.")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ---------- Added To Platform History ----------

def render_history(repo: ShoppingRepository) -> None:
    st.markdown(
        '<div class="section-header"><h2>📦 Added to Platform History</h2></div>',
        unsafe_allow_html=True,
    )
    history = repo.list_history(st.session_state.session_id)
    if not history:
        st.markdown(
            '<div class="empty-state"><div class="icon">📦</div>'
            "No items have been added to marketplace carts yet.</div>",
            unsafe_allow_html=True,
        )
    else:
        for row in history:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.markdown(
                f'{_platform_logo_badge(row["platform"])} '
                f'{_status_badge(row["status"])}',
                unsafe_allow_html=True,
            )
            st.markdown(f"**{row['title']}**")
            st.markdown(
                f'<span class="price-tag">${row["total_cost"]:.2f}</span>',
                unsafe_allow_html=True,
            )
            st.markdown(f"Added on: {row.get('platform_added_date', 'N/A')}")
            st.markdown(f"[🔗 View on {row['platform'].title()}]({row['url']})")
            st.markdown("</div>", unsafe_allow_html=True)


# ---------- History Purge ----------

def render_purge(service: ShoppingGraphService, repo: ShoppingRepository) -> None:
    st.markdown(
        '<div class="section-header"><h2>🗑️ History Purge</h2></div>',
        unsafe_allow_html=True,
    )
    st.write("Remove older added-to-platform records. Human confirmation is required.")

    # --- show all added-to-platform items so user can see what exists ---
    history = repo.list_history(st.session_state.session_id)
    if history:
        st.markdown(f"**{len(history)}** item(s) currently in your Added-to-Platform history:")
        for row in history:
            st.markdown(
                f'<div class="product-card" style="padding:0.8rem 1rem">'
                f'{_platform_logo_badge(row["platform"])} '
                f'**{row["title"]}** — ${row["total_cost"]:.2f} '
                f'(added {row.get("platform_added_date", "N/A")})'
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="empty-state"><div class="icon">🗑️</div>'
            "No items in history to purge.</div>",
            unsafe_allow_html=True,
        )
        return

    st.divider()
    cutoff_days = st.number_input("Purge items older than (days)", min_value=1, max_value=365, value=60)
    preview_count = repo.count_purge_candidates(int(cutoff_days), session_id=st.session_state.session_id)
    st.info(f"📊 {preview_count} record(s) are older than {cutoff_days} days and eligible for purge.")
    if not st.session_state.pending_purge:
        if st.button("🔍 Request Purge Review"):
            preview = service.purge_history(st.session_state.session_id, int(cutoff_days), confirm=False)
            st.session_state.pending_purge = preview.get("purge_count", 0) > 0
            st.session_state.pending_purge_count = preview.get("purge_count", 0)
            st.session_state.purge_cutoff_days = int(cutoff_days)
            if not st.session_state.pending_purge:
                st.info("No records old enough to purge with the selected cutoff.")
            else:
                st.rerun()
    else:
        st.warning(
            f"⚠️ Human confirmation required to purge **{st.session_state.pending_purge_count}** "
            f"records older than {st.session_state.purge_cutoff_days} days."
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Approve Purge", type="primary"):
                result = service.purge_history(
                    st.session_state.session_id,
                    int(st.session_state.purge_cutoff_days),
                    confirm=True,
                )
                st.session_state.pending_purge = False
                st.success(result.get("message", "Purged records."))
                st.rerun()
        with col2:
            if st.button("❌ Reject Purge"):
                st.session_state.pending_purge = False
                st.info("Purge rejected by human reviewer.")
                st.rerun()


# ---------- Settings ----------

def render_settings() -> None:
    settings = get_settings()
    st.markdown(
        '<div class="section-header"><h2>⚙️ Settings</h2></div>',
        unsafe_allow_html=True,
    )
    st.write("Loaded from `.env` and used by the AI Recommender Agent.")
    st.json(
        {
            "shipping_zip": settings.shipping_zip,
            "allowed_platforms": settings.allowed_platforms,
            "recommender_model": settings.recommender_model,
            "max_recommendations": settings.max_recommendations,
            "email_to": settings.email_to,
            "smtp_host": settings.smtp_host,
            "smtp_configured": bool(settings.smtp_username and settings.smtp_app_password),
        }
    )


# ---------- main ----------

def main() -> None:
    init_state()
    service = get_service()
    repo = service.repository
    brand_header()
    sidebar()
    page = st.session_state.page
    if page == "Find Items":
        render_find_items(service, repo)
    elif page == "Cart Review":
        render_cart_review(service, repo)
    elif page == "Added To Platform":
        render_history(repo)
    elif page == "History Purge":
        render_purge(service, repo)
    else:
        render_settings()


if __name__ == "__main__":
    main()
