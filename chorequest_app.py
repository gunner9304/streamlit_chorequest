import os
from datetime import date, timedelta
import pandas as pd
import streamlit as st

# ==================================================
# ChoreQuest Ultimate - Final Editable Version
# Run with: streamlit run chorequest_streamlit_app.py
# ==================================================

st.set_page_config(page_title="ChoreQuest Ultimate", page_icon="🏆", layout="wide")

# ----------------------------
# File paths
# ----------------------------
DATA_DIR = "chorequest_data"
KIDS_FILE = os.path.join(DATA_DIR, "kids.csv")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.csv")
DAILY_FILE = os.path.join(DATA_DIR, "daily_completions.csv")
WEEKLY_FILE = os.path.join(DATA_DIR, "weekly_completions.csv")
PROJECT_FILE = os.path.join(DATA_DIR, "project_completions.csv")
DAILY_TEMPLATE_FILE = os.path.join(DATA_DIR, "daily_tasks.csv")
WEEKLY_TEMPLATE_FILE = os.path.join(DATA_DIR, "weekly_tasks.csv")
PROJECT_TEMPLATE_FILE = os.path.join(DATA_DIR, "project_tasks.csv")

# ----------------------------
# Default data
# ----------------------------
DEFAULT_KIDS = [
    {"kid_name": "Layla", "avatar": "🌟", "color": "#8ecae6"},
    {"kid_name": "Penny", "avatar": "🦋", "color": "#ffb4a2"},
]

DEFAULT_DAILY_TASKS = [
    {"task": "Make Bed"},
    {"task": "Brush Teeth AM"},
    {"task": "Brush Teeth PM"},
    {"task": "Tidy Bedroom"},
    {"task": "Make Lunch"},
    {"task": "Make Coffee"},
]

DEFAULT_WEEKLY_TASKS = [
    {"task": "Kitchen Reset", "value": 2},
    {"task": "Common Area Tidying", "value": 2},
    {"task": "Trash & Recycling", "value": 2},
    {"task": "Pet Area Clean Up", "value": 2},
    {"task": "Full Laundry Cycle", "value": 2},
    {"task": "Bathroom Refresh", "value": 2},
    {"task": "Floors-Sweeping and Mopping", "value": 5},
    {"task": "Wash Bedding", "value": 5},
    {"task": "Basement Clean including Bathroom", "value": 5},
]

DEFAULT_PROJECT_TASKS = [
    {"task": "Meal Prep Night", "value": 10},
    {"task": "Vehicle Clean", "value": 10},
    {"task": "Yard Work", "value": 10},
    {"task": "Fridge Purge", "value": 8},
    {"task": "Clean Baseboards", "value": 10},
    {"task": "Clean Up Dog Poop", "value": 10},
]

DEFAULT_SETTINGS = [
    {"key": "perfect_bonus", "value": "5"},
    {"key": "parent_pin", "value": "1234"},
]

# ----------------------------
# Styling
# ----------------------------
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    }
    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }
    .cq-hero {
        background: linear-gradient(135deg, #1d4ed8 0%, #7c3aed 100%);
        padding: 1.4rem 1.6rem;
        border-radius: 22px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        margin-bottom: 1rem;
    }
    .cq-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        margin-bottom: 0.9rem;
    }
    .cq-stat {
        background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.04));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        min-height: 104px;
    }
    .cq-label {
        font-size: 0.82rem;
        opacity: 0.8;
        margin-bottom: 0.2rem;
    }
    .cq-value {
        font-size: 1.8rem;
        font-weight: 700;
    }
    .cq-sub {
        font-size: 0.9rem;
        opacity: 0.82;
    }
    .cq-task-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
    }
    .cq-rule {
        background: rgba(34,197,94,0.10);
        border: 1px solid rgba(34,197,94,0.18);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.8rem;
    }
    .cq-mini {
        font-size: 0.84rem;
        opacity: 0.8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Helpers
# ----------------------------
def monday_of_week(any_date: date) -> date:
    return any_date - timedelta(days=any_date.weekday())


def sunday_of_week(any_date: date) -> date:
    return monday_of_week(any_date) + timedelta(days=6)


def load_csv(path, columns):
    if os.path.exists(path):
        df = pd.read_csv(path)
        for col in columns:
            if col not in df.columns:
                df[col] = ""
        return df[columns]
    return pd.DataFrame(columns=columns)


def save_csv(df, path):
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(path, index=False)


def clean_text(value):
    return str(value).strip()


def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(KIDS_FILE):
        save_csv(pd.DataFrame(DEFAULT_KIDS), KIDS_FILE)

    if not os.path.exists(SETTINGS_FILE):
        save_csv(pd.DataFrame(DEFAULT_SETTINGS), SETTINGS_FILE)

    if not os.path.exists(DAILY_TEMPLATE_FILE):
        save_csv(pd.DataFrame(DEFAULT_DAILY_TASKS), DAILY_TEMPLATE_FILE)

    if not os.path.exists(WEEKLY_TEMPLATE_FILE):
        save_csv(pd.DataFrame(DEFAULT_WEEKLY_TASKS), WEEKLY_TEMPLATE_FILE)

    if not os.path.exists(PROJECT_TEMPLATE_FILE):
        save_csv(pd.DataFrame(DEFAULT_PROJECT_TASKS), PROJECT_TEMPLATE_FILE)

    if not os.path.exists(DAILY_FILE):
        save_csv(pd.DataFrame(columns=["kid", "task", "date", "week_start", "completed"]), DAILY_FILE)

    if not os.path.exists(WEEKLY_FILE):
        save_csv(pd.DataFrame(columns=["kid", "task", "value", "week_start", "completed_date", "completed"]), WEEKLY_FILE)

    if not os.path.exists(PROJECT_FILE):
        save_csv(pd.DataFrame(columns=["kid", "task", "value", "week_start", "completed_date", "completed"]), PROJECT_FILE)


def get_settings_dict():
    df = load_csv(SETTINGS_FILE, ["key", "value"])
    return dict(zip(df["key"], df["value"]))


def get_kids():
    return load_csv(KIDS_FILE, ["kid_name", "avatar", "color"])


def get_daily_templates():
    df = load_csv(DAILY_TEMPLATE_FILE, ["task"])
    df["task"] = df["task"].astype(str).str.strip()
    return df[df["task"] != ""].drop_duplicates(subset=["task"])


def get_weekly_templates():
    df = load_csv(WEEKLY_TEMPLATE_FILE, ["task", "value"])
    df["task"] = df["task"].astype(str).str.strip()
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    return df[df["task"] != ""].drop_duplicates(subset=["task"])


def get_project_templates():
    df = load_csv(PROJECT_TEMPLATE_FILE, ["task", "value"])
    df["task"] = df["task"].astype(str).str.strip()
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    return df[df["task"] != ""].drop_duplicates(subset=["task"])


def get_or_seed_daily_for_week(kid: str, week_start: date):
    df = load_csv(DAILY_FILE, ["kid", "task", "date", "week_start", "completed"])
    templates = get_daily_templates()
    week_str = str(week_start)
    existing = df[(df["kid"] == kid) & (df["week_start"] == week_str)]

    rows = []
    for offset in range(7):
        day = week_start + timedelta(days=offset)
        for task in templates["task"].tolist():
            mask = (
                (existing["date"] == str(day))
                & (existing["task"] == task)
            )
            if existing[mask].empty:
                rows.append(
                    {
                        "kid": kid,
                        "task": task,
                        "date": str(day),
                        "week_start": week_str,
                        "completed": False,
                    }
                )

    if rows:
        df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
        save_csv(df, DAILY_FILE)
        df = load_csv(DAILY_FILE, ["kid", "task", "date", "week_start", "completed"])
    return df


def get_or_seed_template_items_for_week(file_path: str, kid: str, week_start: date, template_df: pd.DataFrame):
    df = load_csv(file_path, ["kid", "task", "value", "week_start", "completed_date", "completed"])
    week_str = str(week_start)
    existing = df[(df["kid"] == kid) & (df["week_start"] == week_str)]

    rows = []
    for _, row in template_df.iterrows():
        task = clean_text(row["task"])
        value = float(row["value"])
        mask = existing["task"] == task
        if existing[mask].empty:
            rows.append(
                {
                    "kid": kid,
                    "task": task,
                    "value": value,
                    "week_start": week_str,
                    "completed_date": "",
                    "completed": False,
                }
            )

    if rows:
        df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
        save_csv(df, file_path)
        df = load_csv(file_path, ["kid", "task", "value", "week_start", "completed_date", "completed"])
    return df


def get_or_seed_weekly_for_week(kid: str, week_start: date):
    return get_or_seed_template_items_for_week(WEEKLY_FILE, kid, week_start, get_weekly_templates())


def get_or_seed_projects_for_week(kid: str, week_start: date):
    return get_or_seed_template_items_for_week(PROJECT_FILE, kid, week_start, get_project_templates())


def toggle_daily(kid: str, task: str, target_date: date, value: bool):
    df = load_csv(DAILY_FILE, ["kid", "task", "date", "week_start", "completed"])
    mask = (df["kid"] == kid) & (df["task"] == task) & (df["date"] == str(target_date))
    df.loc[mask, "completed"] = bool(value)
    save_csv(df, DAILY_FILE)


def toggle_weekly(file_path: str, kid: str, task: str, week_start: date, value: bool):
    df = load_csv(file_path, ["kid", "task", "value", "week_start", "completed_date", "completed"])
    mask = (df["kid"] == kid) & (df["task"] == task) & (df["week_start"] == str(week_start))
    df.loc[mask, "completed"] = bool(value)
    df.loc[mask, "completed_date"] = str(date.today()) if value else ""
    save_csv(df, file_path)


def get_daily_status(kid: str, target_date: date):
    week_start = monday_of_week(target_date)
    df = get_or_seed_daily_for_week(kid, week_start)
    target = df[(df["kid"] == kid) & (df["date"] == str(target_date))].copy()
    target["completed"] = target["completed"].astype(str).str.lower().isin(["true", "1", "yes"]) if target["completed"].dtype == object else target["completed"]
    return target.sort_values("task")


def day_complete(kid: str, target_date: date):
    day_df = get_daily_status(kid, target_date)
    if day_df.empty:
        return False
    return bool(day_df["completed"].all())


def current_week_completion_count(kid: str, week_start: date):
    count = 0
    for i in range(7):
        d = week_start + timedelta(days=i)
        if day_complete(kid, d):
            count += 1
    return count


def today_streak_in_week(kid: str, week_start: date, today: date):
    streak = 0
    current = min(today, sunday_of_week(week_start))
    while current >= week_start:
        if day_complete(kid, current):
            streak += 1
            current -= timedelta(days=1)
        else:
            break
    return streak


def weekly_earned(kid: str, week_start: date):
    week_str = str(week_start)
    weekly = get_or_seed_weekly_for_week(kid, week_start)
    projects = get_or_seed_projects_for_week(kid, week_start)
    weekly["completed"] = weekly["completed"].astype(str).str.lower().isin(["true", "1", "yes"]) if weekly["completed"].dtype == object else weekly["completed"]
    projects["completed"] = projects["completed"].astype(str).str.lower().isin(["true", "1", "yes"]) if projects["completed"].dtype == object else projects["completed"]

    w = weekly[(weekly["kid"] == kid) & (weekly["week_start"] == week_str) & (weekly["completed"] == True)]
    p = projects[(projects["kid"] == kid) & (projects["week_start"] == week_str) & (projects["completed"] == True)]
    weekly_total = float(pd.to_numeric(w["value"], errors="coerce").fillna(0).sum())
    project_total = float(pd.to_numeric(p["value"] , errors="coerce").fillna(0).sum())
    return round(weekly_total + project_total, 2), round(weekly_total, 2), round(project_total, 2)


def unlocked_amount(kid: str, week_start: date, perfect_bonus: float):
    earned, _, _ = weekly_earned(kid, week_start)
    full_days = current_week_completion_count(kid, week_start)
    if full_days >= 7:
        return round(earned + perfect_bonus, 2), True
    return 0.0, False


def render_stat(label, value, sub=""):
    st.markdown(
        f"""
        <div class='cq-stat'>
            <div class='cq-label'>{label}</div>
            <div class='cq-value'>{value}</div>
            <div class='cq-sub'>{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_task_card(title, meta="", extra=""):
    st.markdown(
        f"""
        <div class='cq-card'>
            <div class='cq-task-title'>{title}</div>
            <div class='cq-mini'>{meta}</div>
            <div class='cq-mini' style='margin-top:0.35rem'>{extra}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def normalize_kids_editor(df):
    df = df.copy()
    df = df.dropna(subset=["kid_name"])
    df["kid_name"] = df["kid_name"].astype(str).str.strip()
    df["avatar"] = df["avatar"].astype(str).fillna("🙂")
    df["color"] = df["color"].astype(str).fillna("#8ecae6")
    df = df[df["kid_name"] != ""]
    df = df.drop_duplicates(subset=["kid_name"], keep="first")
    return df[["kid_name", "avatar", "color"]]


def normalize_task_editor(df, with_value=False):
    df = df.copy()
    df = df.dropna(subset=["task"])
    df["task"] = df["task"].astype(str).str.strip()
    df = df[df["task"] != ""]
    df = df.drop_duplicates(subset=["task"], keep="first")
    if with_value:
        df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0).round(2)
        return df[["task", "value"]]
    return df[["task"]]


# ----------------------------
# App start
# ----------------------------
ensure_files()
settings = get_settings_dict()
perfect_bonus = float(settings.get("perfect_bonus", "5"))
parent_pin = str(settings.get("parent_pin", "1234"))

kids_df = get_kids()
kid_names = kids_df["kid_name"].tolist()
if not kid_names:
    st.error("No kids found. Add at least one child in the Parent Zone.")
    st.stop()

selected_kid = st.sidebar.selectbox("Choose player", kid_names)
view_mode = st.sidebar.radio("Open", ["Kid Zone", "Parent Zone", "Rules"])

kid_row = kids_df[kids_df["kid_name"] == selected_kid].iloc[0]
avatar = kid_row["avatar"]

today = date.today()
week_start = monday_of_week(today)
week_end = sunday_of_week(today)
week_label = f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d')}"

current_day_df = get_daily_status(selected_kid, today)
weekly_df = get_or_seed_weekly_for_week(selected_kid, week_start)
project_df = get_or_seed_projects_for_week(selected_kid, week_start)
daily_templates = get_daily_templates()
weekly_templates = get_weekly_templates()
project_templates = get_project_templates()

full_days = current_week_completion_count(selected_kid, week_start)
streak = today_streak_in_week(selected_kid, week_start, today)
earned_total, weekly_total, project_total = weekly_earned(selected_kid, week_start)
unlocked_total, is_unlocked = unlocked_amount(selected_kid, week_start, perfect_bonus)
remaining_days = max(0, 7 - full_days)
daily_done_today = int(current_day_df["completed"].sum()) if not current_day_df.empty else 0

st.markdown(
    f"""
    <div class='cq-hero'>
        <div style='font-size:1rem; opacity:0.88;'>🏆 ChoreQuest Ultimate</div>
        <div style='font-size:2rem; font-weight:800; margin-top:0.25rem;'>{avatar} {selected_kid}</div>
        <div style='font-size:1rem; opacity:0.92; margin-top:0.15rem;'>Weekly quest window: {week_label}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if view_mode == "Kid Zone":
    top1, top2, top3, top4 = st.columns(4)
    with top1:
        render_stat("Today's Progress", f"{daily_done_today}/{len(daily_templates)}", "Daily essentials completed")
    with top2:
        render_stat("Current Streak", f"{streak}", "Consecutive fully-complete days")
    with top3:
        render_stat("Earned This Week", f"${earned_total:.2f}", f"Weekly ${weekly_total:.2f} + Project ${project_total:.2f}")
    with top4:
        render_stat("Unlocked", f"${unlocked_total:.2f}" if is_unlocked else "🔒 Locked", f"Perfect week bonus = ${perfect_bonus:.2f}")

    st.markdown("### Daily Essentials")
    st.progress(full_days / 7)
    st.caption(f"Perfect week progress: {full_days}/7 complete days. {remaining_days} more full day(s) needed.")

    daily_cols = st.columns(2)
    for idx, row in current_day_df.reset_index(drop=True).iterrows():
        checked = bool(row["completed"])
        with daily_cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"**{row['task']}**")
                st.caption("Counts toward the 7-day perfect streak")
                new_val = st.checkbox("Complete", value=checked, key=f"daily_{selected_kid}_{row['task']}_{today}")
                if new_val != checked:
                    toggle_daily(selected_kid, row["task"], today, new_val)
                    st.rerun()

    st.markdown("### Weekly Responsibilities")
    active_weekly = weekly_df[(weekly_df["kid"] == selected_kid) & (weekly_df["week_start"] == str(week_start))].copy().sort_values("task")
    weekly_cols = st.columns(2)
    for idx, row in active_weekly.reset_index(drop=True).iterrows():
        checked = str(row["completed"]).lower() in ["true", "1", "yes"] if isinstance(row["completed"], str) else bool(row["completed"])
        with weekly_cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"**{row['task']}** — ${float(row['value']):.2f}")
                st.caption("Weekly earning task")
                new_val = st.checkbox("Completed", value=checked, key=f"weekly_{selected_kid}_{row['task']}_{week_start}")
                if new_val != checked:
                    toggle_weekly(WEEKLY_FILE, selected_kid, row["task"], week_start, new_val)
                    st.rerun()

    st.markdown("### Bonus Project Chores")
    active_projects = project_df[(project_df["kid"] == selected_kid) & (project_df["week_start"] == str(week_start))].copy().sort_values("task")
    project_cols = st.columns(2)
    for idx, row in active_projects.reset_index(drop=True).iterrows():
        checked = str(row["completed"]).lower() in ["true", "1", "yes"] if isinstance(row["completed"], str) else bool(row["completed"])
        with project_cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"**{row['task']}** — ${float(row['value']):.2f}")
                st.caption("Optional extra earning")
                new_val = st.checkbox("Completed", value=checked, key=f"project_{selected_kid}_{row['task']}_{week_start}")
                if new_val != checked:
                    toggle_weekly(PROJECT_FILE, selected_kid, row["task"], week_start, new_val)
                    st.rerun()

    st.markdown("### Week-at-a-Glance")
    week_summary_cols = st.columns(7)
    for i in range(7):
        d = week_start + timedelta(days=i)
        done = day_complete(selected_kid, d)
        label = d.strftime("%a")
        icon = "✅" if done else "⬜"
        with week_summary_cols[i]:
            st.markdown(
                f"<div class='cq-card' style='text-align:center; padding:0.7rem 0.3rem'><div>{label}</div><div style='font-size:1.5rem'>{icon}</div><div class='cq-mini'>{d.strftime('%b %d')}</div></div>",
                unsafe_allow_html=True,
            )

elif view_mode == "Parent Zone":
    pin_try = st.sidebar.text_input("Parent PIN", type="password")
    if pin_try != parent_pin:
        st.warning("Enter the parent PIN in the sidebar to open the Parent Zone.")
        st.stop()

    st.markdown("### Parent Command Center")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Kids", "Task Lists", "This Week", "Settings"])

    with tab1:
        overview_cards = st.columns(4)
        family_earned = 0.0
        family_unlocked = 0.0
        perfect_count = 0
        for kid in kid_names:
            earned, _, _ = weekly_earned(kid, week_start)
            unlocked, ok = unlocked_amount(kid, week_start, perfect_bonus)
            family_earned += earned
            family_unlocked += unlocked
            if ok:
                perfect_count += 1

        with overview_cards[0]:
            render_stat("Family Earned", f"${family_earned:.2f}", "All weekly + project chores")
        with overview_cards[1]:
            render_stat("Family Unlocked", f"${family_unlocked:.2f}", "Available to cash out")
        with overview_cards[2]:
            render_stat("Perfect Weeks", str(perfect_count), "Kids who hit 7/7")
        with overview_cards[3]:
            render_stat("Reset Day", "Sunday", "New week starts automatically on Monday")

        summary_rows = []
        for kid in kid_names:
            kid_days = current_week_completion_count(kid, week_start)
            kid_streak = today_streak_in_week(kid, week_start, today)
            earned, weekly_amt, project_amt = weekly_earned(kid, week_start)
            unlocked, ok = unlocked_amount(kid, week_start, perfect_bonus)
            summary_rows.append(
                {
                    "Kid": kid,
                    "Complete Days": kid_days,
                    "Current Streak": kid_streak,
                    "Weekly Earned": weekly_amt,
                    "Project Earned": project_amt,
                    "Unlocked": unlocked,
                    "Perfect Week": "Yes" if ok else "No",
                }
            )
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("#### Edit Kid Profiles")
        edited_kids = st.data_editor(kids_df.copy(), use_container_width=True, num_rows="dynamic", key="kids_editor")
        if st.button("Save Kid Profiles"):
            cleaned = normalize_kids_editor(edited_kids)
            if cleaned.empty:
                st.error("At least one kid is required.")
            else:
                save_csv(cleaned, KIDS_FILE)
                st.success("Kid profiles saved. Refresh the app to reload the sidebar list.")

    with tab3:
        sub1, sub2, sub3 = st.tabs(["Daily Essentials", "Weekly Responsibilities", "Project Chores"])

        with sub1:
            st.markdown("Edit the daily tasks that must all be completed for a day to count toward the 7-day streak.")
            daily_edit = st.data_editor(daily_templates.copy(), use_container_width=True, num_rows="dynamic", key="daily_editor")
            if st.button("Save Daily Essentials"):
                cleaned = normalize_task_editor(daily_edit, with_value=False)
                if cleaned.empty:
                    st.error("At least one daily task is required.")
                else:
                    save_csv(cleaned, DAILY_TEMPLATE_FILE)
                    st.success("Daily essentials saved. New tasks will appear for the current and future weeks after refresh.")

        with sub2:
            st.markdown("Edit the weekly earning chores and dollar values.")
            weekly_edit = st.data_editor(weekly_templates.copy(), use_container_width=True, num_rows="dynamic", key="weekly_editor")
            if st.button("Save Weekly Responsibilities"):
                cleaned = normalize_task_editor(weekly_edit, with_value=True)
                if cleaned.empty:
                    st.error("At least one weekly task is required.")
                else:
                    save_csv(cleaned, WEEKLY_TEMPLATE_FILE)
                    st.success("Weekly responsibilities saved.")

        with sub3:
            st.markdown("Edit the optional bigger-ticket chores and values.")
            project_edit = st.data_editor(project_templates.copy(), use_container_width=True, num_rows="dynamic", key="project_editor")
            if st.button("Save Project Chores"):
                cleaned = normalize_task_editor(project_edit, with_value=True)
                if cleaned.empty:
                    st.error("At least one project chore is required.")
                else:
                    save_csv(cleaned, PROJECT_TEMPLATE_FILE)
                    st.success("Project chores saved.")

    with tab4:
        st.markdown("#### Current Week Task Status")
        week_kid = st.selectbox("View this week's task state for", kid_names, key="week_kid_select")
        week_daily = get_daily_status(week_kid, today)
        week_weekly = get_or_seed_weekly_for_week(week_kid, week_start)
        week_projects = get_or_seed_projects_for_week(week_kid, week_start)

        st.markdown("**Today's Daily Essentials**")
        st.dataframe(week_daily.sort_values("task"), use_container_width=True, hide_index=True)

        st.markdown("**This Week's Weekly Responsibilities**")
        st.dataframe(
            week_weekly[(week_weekly["kid"] == week_kid) & (week_weekly["week_start"] == str(week_start))].sort_values("task"),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("**This Week's Project Chores**")
        st.dataframe(
            week_projects[(week_projects["kid"] == week_kid) & (week_projects["week_start"] == str(week_start))].sort_values("task"),
            use_container_width=True,
            hide_index=True,
        )

    with tab5:
        st.markdown("#### App Settings")
        new_bonus = st.number_input("Perfect Week Bonus ($)", min_value=0.0, value=float(perfect_bonus), step=1.0)
        new_pin = st.text_input("Parent PIN", value=parent_pin)
        if st.button("Save Settings"):
            settings_df = pd.DataFrame([
                {"key": "perfect_bonus", "value": str(new_bonus)},
                {"key": "parent_pin", "value": str(new_pin)},
            ])
            save_csv(settings_df, SETTINGS_FILE)
            st.success("Settings saved.")

elif view_mode == "Rules":
    st.markdown("### How ChoreQuest Works")
    st.markdown(
        f"""
        <div class='cq-rule'>
            <strong>1. Daily essentials drive the streak.</strong><br>
            A day only counts if all {len(daily_templates)} daily tasks are completed.
        </div>
        <div class='cq-rule'>
            <strong>2. Weekly chores earn money.</strong><br>
            Weekly responsibilities and bonus project chores build the money total for the week.
        </div>
        <div class='cq-rule'>
            <strong>3. Money stays locked until perfection.</strong><br>
            Hit 7 complete days in the week to unlock all earnings plus the ${perfect_bonus:.2f} perfect-week bonus.
        </div>
        <div class='cq-rule'>
            <strong>4. Sunday is the finish line.</strong><br>
            The app tracks weeks Monday through Sunday. A new quest week starts automatically every Monday.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        render_task_card("Daily Essentials", "The non-negotiables", ", ".join(daily_templates["task"].tolist()) or "No daily tasks configured")
        render_task_card("Weekly Responsibilities", "The main earners", ", ".join(weekly_templates["task"].tolist()) or "No weekly tasks configured")
    with col_b:
        render_task_card("Project Chores", "Big effort, bigger payout", ", ".join(project_templates["task"].tolist()) or "No project chores configured")
        render_task_card("Reward Logic", "Consistency wins", f"7/7 complete days = unlock everything + ${perfect_bonus:.2f}")

st.markdown("---")
st.caption("ChoreQuest Ultimate is designed to reward consistency first, then effort. Clean app, clear expectations, strong incentive.")
