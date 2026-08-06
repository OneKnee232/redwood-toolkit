import streamlit as st
import urllib.parse
from datetime import datetime, timedelta
import pytz
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="The Redwood Group | Sales Toolkit", page_icon="🌲", layout="wide")

# --- CUSTOM CSS (THE READABILITY FIX) ---
st.markdown("""
    <style>
    pre {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        overflow-x: hidden !important;
    }
    code {
        white-space: pre-wrap !important;
        font-family: system-ui, -apple-system, sans-serif !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- AGENT PORTAL (SIDEBAR) ---
st.sidebar.title("🌲 Agent Portal")
agent_input = st.sidebar.text_input("Your Name:", placeholder="e.g., Rick Thomas")

# Dynamic Agent Name Variable
a_name = agent_input.strip() if agent_input else "[Agent Name]"

st.sidebar.markdown("---")

# --- AUTO-SAVING NOTES TAB ---
st.sidebar.header("📝 Scratchpad")

notes_html = """
    <div style="width: 100%; height: 100%;">
        <textarea id="agentNotes" 
        style="width: 100%; height: 400px; background-color: #1e1e24; color: #ffffff; padding: 12px; border-radius: 8px; border: 1px solid #4b4b4b; font-family: system-ui, sans-serif; font-size: 14px; resize: vertical;" 
        placeholder="Paste customer details, MPANs, or quick notes here..."></textarea>
    </div>
    <script>
        const notesField = document.getElementById('agentNotes');
        notesField.value = localStorage.getItem('redwood_agent_notes') || '';
        notesField.addEventListener('input', function() {
            localStorage.setItem('redwood_agent_notes', notesField.value);
        });
    </script>
"""
with st.sidebar:
    components.html(notes_html, height=420)

# --- MAIN DASHBOARD ---
st.title("🌲 The Redwood Group - Sales Intelligence Toolkit")

# --- TOP FORM (To generate variables used everywhere) ---
with st.form("prospect_form"):
    form_col1, form_col2 = st.columns(2)
    with form_col1:
        company_name = st.text_input("Company Name", placeholder="e.g., Apex Catering Ltd")
        customer_name = st.text_input("Decision Maker Name", placeholder="e.g., John")
    with form_col2:
        business_type = st.text_input("Industry / Sector", placeholder="e.g., Restaurant, Retail")
        location = st.text_input("Town / Postcode", placeholder="e.g., Manchester")
    
    submit_button = st.form_submit_button(label="Load Customer Profile")

# Dynamic Variables for Scripts
c_name = customer_name.strip() if customer_name else "[Name]"
comp = company_name.strip() if company_name else "[Company]"
loc = location.strip() if location else "site"

st.markdown("---")

# --- SECTION 1: THE OPENING PITCH ---
st.header("📞 1. The Opening Pitch")

intro_script = f"""Hiya, is that {c_name}?

(Wait for them to answer)

Perfect! It's just a quick call regarding the energy down at {comp}, is that something you deal with?

(Wait for them to answer)

Brilliant, you're speaking to {a_name} at The Redwood Group. We're calling as we believe you're currently in your renewal window, does that sound about right?

(Wait for them to answer)

The only reason I'm asking is because we're looking to gather some quotes for your renewal. Who are you currently with? 

(Wait for them to name the supplier)

How have you found them? ... We actually work alongside all the major suppliers in the UK and get preferential rates, so if you have a supplier in mind I can prioritise pricing from them. Do you have an end date for your current supply?

(Listen for end date / MPAN)

If I send you over an email, would you be able to reply with a copy of a recent utility bill? Or would WhatsApp be easier for you?"""

st.code(intro_script, language="text", wrap_lines=True)

st.markdown("---")

# --- TOP LAYOUT: 2 COLUMNS ---
col1, col2 = st.columns([1.2, 1])

# COLUMN 1: LIVE INTELLIGENCE & MAXCONTACT NOTES
with col1:
    st.header("🏢 2. Live Intelligence & CRM Notes")

    if submit_button and company_name:
        business_lower = business_type.lower()
        is_hosp = any(w in business_lower for w in ["restaurant", "pub", "bar", "cafe", "food", "hotel"])
        is_retail = any(w in business_lower for w in ["shop", "store", "retail", "salon"])
        is_office = any(w in business_lower for w in ["office", "consultancy", "tech", "agency"])
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("⚡ Energy", "High Priority" if not is_office else "Medium Match")
        c2.metric("💧 Water/Waste", "High Priority" if is_hosp else "Low Match")
        c3.metric("💳 Merchant", "Critical" if (is_hosp or is_retail) else "Low Match")
        c4.metric("🌐 Broadband", "High Priority" if is_office else "Standard")
        
        crm_note = f"Agent: {a_name}\nCompany: {company_name}\nContact: {c_name}\nSector: {business_type}\nLocation: {location}\nAction: Pitched renewal window. Pushed for MPAN/Bill.\nCross-Sell Targets: Energy, Merchant Services."
        st.code(crm_note, language="text", wrap_lines=True)

# COLUMN 2: REAL-WORLD MARKET URGENCY
with col2:
    st.header("🌍 3. Market Urgency")
    
    st.markdown("**The Global Conflict & Inflation Pitch:**")
    war_pitch = f"With the ongoing geopolitical conflicts and inflation squeezing the markets, wholesale gas and electricity prices are incredibly volatile right now. Suppliers are using this as an excuse to hike up out-of-contract rates. My job isn't just to quote you; it's to lock in a protective shield around your business overheads before the next market spike hits."
    st.code(war_pitch, language="text", wrap_lines=True)
    
    st.markdown("**The 12-Month Window Reality:**")
    window_pitch = f"A lot of directors don't realize this, {c_name}, but because of the current inflation crisis, suppliers have opened up their renewal windows a full 12 months in advance. If your contract ends anywhere in the next year, we can secure today's dipped rates now, rather than leaving you at the mercy of whatever the global market does next year."
    st.code(window_pitch, language="text", wrap_lines=True)

st.markdown("---")

# --- MIDDLE LAYOUT: STRATEGIC CALLBACKS & QUALIFICATION ---
st.header("📅 4. Strategic Callbacks")

colX, colY = st.columns(2)

with colX:
    with st.expander("❓ 'Price vs. Supplier' Qualifier"):
        script_qual = f"Just before we run the numbers, {c_name}, let me ask you: are you strictly looking for a better price right now to combat inflation, or is there a certain supplier in the market you'd actually prefer to move to?"
        st.code(script_qual, language="text", wrap_lines=True)

    with st.expander("⏳ Pinning the Callback (No 'Next Week')"):
        script_pin = f"I don't want to just vaguely call you 'next week' and catch you at another bad time. Let's lock in 5 minutes. Would Tuesday or Thursday be better for you? ... Perfect, and what time on that day lets you actually sit down for a moment?"
        st.code(script_pin, language="text", wrap_lines=True)

with colY:
    with st.expander("📆 'Admin Day' Empathy Play"):
        script_admin = f"I completely understand you have a business to run, {c_name}, and I don't want to take you off the floor. Do you have a specific 'admin day' where you actually sit down to look at the paperwork? I just need a few minutes of your time then."
        st.code(script_admin, language="text", wrap_lines=True)

st.markdown("---")

# --- CALLBACK SCHEDULER (CALENDAR LINKS) ---
st.header("🗓️ 5. Callback Scheduler")

call_col1, call_col2, call_col3 = st.columns(3)

with call_col1:
    call_date = st.date_input("Callback Date")
with call_col2:
    call_time_uk = st.time_input("Agreed UK Time (Local to Customer)")
with call_col3:
    meeting_duration = st.selectbox("Duration", [10, 15, 30], index=1, format_func=lambda x: f"{x} mins")

if st.button("Generate Calendar Links"):
    uk_tz = pytz.timezone("Europe/London")
    local_dt = datetime.combine(call_date, call_time_uk)
    uk_dt = uk_tz.localize(local_dt)
    utc_start = uk_dt.astimezone(pytz.utc)
    utc_end = utc_start + timedelta(minutes=meeting_duration)
    
    fmt_start = utc_start.strftime('%Y%m%dT%H%M%SZ')
    fmt_end = utc_end.strftime('%Y%m%dT%H%M%SZ')
    
    event_title = f"Callback: The Redwood Group <> {comp}"
    event_desc = f"Agent: {a_name}\nContact: {c_name}\nDiscussion regarding commercial overheads and 12-month renewal window."
    
    gcal_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={urllib.parse.quote(event_title)}&dates={fmt_start}/{fmt_end}&details={urllib.parse.quote(event_desc)}"
    
    out_start = utc_start.strftime('%Y-%m-%dT%H:%M:%SZ')
    out_end = utc_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    outlook_url = f"https://outlook.office.com/calendar/0/deeplink/compose?path=/calendar/action/compose&rru=addevent&subject={urllib.parse.quote(event_title)}&startdt={out_start}&enddt={out_end}&body={urllib.parse.quote(event_desc)}"
    
    link_colA, link_colB = st.columns(2)
    with link_colA:
        st.markdown(f"[📅 Add to Google Calendar]({gcal_url})", unsafe_allow_html=True)
        st.code(f"Email Link to Client (Google):\n{gcal_url}", language="text", wrap_lines=True)
    with link_colB:
        st.markdown(f"[📨 Add to Outlook]({outlook_url})", unsafe_allow_html=True)
        st.code(f"Email Link to Client (Outlook):\n{outlook_url}", language="text", wrap_lines=True)

st.markdown("---")

# --- INTERACTIVE PIVOT BOARD ---
st.header("🎯 6. Interactive Pivot Board")

colA, colB = st.columns(2)

with colA:
    with st.expander("🚨 'I won't send a bill / too much hassle'"):
        script_1 = f"I completely understand data privacy, {c_name}, and I know you don't have time to dig through files. Just look at the top left of your statement for your MPAN number (or meter serial number) and tell me your contract end date. That's all my pricing desk needs to run a blind check against the current inflated market."
        st.code(script_1, language="text", wrap_lines=True)
    
    with st.expander("🚨 'We’re already locked into a contract'"):
        script_2 = f"That’s completely normal, {c_name}. But because of the global tensions pushing up energy costs, suppliers have opened their renewal windows 12 months early. If your end date drops within that window, we lock in today's rates before inflation drives them higher. What month does yours end?"
        st.code(script_2, language="text", wrap_lines=True)

    with st.expander("💳 Pivot to Merchant Services"):
        script_5 = f"Understood on the energy, {c_name}. Since we manage all site overheads at The Redwood Group, we're seeing businesses in your sector getting hammered by card terminal fees right now due to inflation. Who currently provides your merchant services?"
        st.code(script_5, language="text", wrap_lines=True)

with colB:
    with st.expander("🚨 'Just email me your prices'"):
        script_3 = f"I can definitely do that, {c_name}, but energy prices shift by the hour based on the wholesale market. If I send a generic rate sheet, it won't match your actual meter profile. Let's grab your MPAN right now while we're on the phone, and I'll text you a custom, verified price check in 10 minutes. Fair?"
        st.code(script_3, language="text", wrap_lines=True)
        
    with st.expander("🚨 'Call me back next year'"):
        script_4 = f"Will do. But just a heads-up, {c_name}, wholesale prices are dipping right now amidst all the inflation chaos. If we log your meter number today, my system will auto-alert you the second the market hits the floor, rather than guessing next year. Got your meter serial number handy?"
        st.code(script_4, language="text", wrap_lines=True)
        
    with st.expander("🆘 CALL RESCUE (Hanging up)"):
        script_6 = f"{c_name}, I can hear I've caught you at the absolute worst time, and you're probably getting ten calls a day like this. If I promise to get off the phone in exactly 30 seconds, can I ask you just one direct question about how inflation is impacting your site?"
        st.code(script_6, language="text", wrap_lines=True)

st.markdown("---")

# --- WHATSAPP QUICK-MESSAGE GENERATOR ---
st.header("📱 7. WhatsApp Internal Handover")

wa_col1, wa_col2 = st.columns(2)
with wa_col1:
    wa_product = st.radio(
        "Product Statement Needed:",
        ["⚡ Electricity", "🔥 Gas", "💳 Merchant Services", "💧 Water / Waste"]
    )
with wa_col2:
    wa_number = st.text_input("Customer Mobile Number:", placeholder="e.g., 07712 345 678")

if wa_product == "⚡ Electricity" or wa_product == "🔥 Gas":
    wa_msg = f"Hi {c_name}, it's {a_name} from The Redwood Group! Great catching up today. As discussed, just drop a quick photo of your latest {wa_product.lower().replace('⚡ ', '').replace('🔥 ', '')} bill here (or just the MPAN/MPRN meter number and contract end date). I'll run the numbers against the current market and send over the comparison. Thanks!"

elif wa_product == "💳 Merchant Services":
    wa_msg = f"Hi {c_name}, it's {a_name} from The Redwood Group! Great chatting earlier. As promised, just send over a quick snap of a recent card machine statement here. I'll get our pricing desk to run a free audit on your transaction fees to see how much we can shave off. Speak soon!"

elif wa_product == "💧 Water / Waste":
    wa_msg = f"Hi {c_name}, {a_name} here from The Redwood Group! Thanks for your time today. Just drop a quick photo of your last water/waste bill here and I'll check if we can consolidate those costs and get you on a better tariff. Cheers!"

fallback_number = wa_number if wa_number else "[Insert Number]"

internal_handover = f"""Please send WhatsApp to: {fallback_number}
Customer Name: {c_name}
Company: {comp}

Message to send:
"{wa_msg}"
"""

st.code(internal_handover, language="text", wrap_lines=True)
