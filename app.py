import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import io
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Futures Teaching & Practice Lab")

mode = st.sidebar.radio("Mode", ["Instructor Demo","Student Practice"])

topic = st.sidebar.radio(
    "Select Module",
    [
        "1. Why Futures",
        "2. Futures Pricing",
        "3. MTM & Margins",
        "4. Trading P&L",
        "5. Trading Strategy Builder",
        "6. Hedging Strategy Builder",
        "7. Optimal Hedge Ratio",
        "8. Basis & Convergence",
        "9. Basis Risk",
        "10. Rolling Futures",
        "11. Matching System",
        "12. Real-World Cases",
        "13. Advanced Strategies",
        "14. Quiz & Certificate"
    ]
)

# =====================================================
# 1 WHY FUTURES
# =====================================================
if topic == "1. Why Futures":
    st.header("Why Futures Exist")
    st.write("""
Hedgers transfer risk  
Speculators take risk  
Arbitrageurs align prices  
""")

# =====================================================
# 2 PRICING
# =====================================================
elif topic == "2. Futures Pricing":
    st.header("Cost-of-Carry Pricing")
    st.latex("F = S(1+r-c)^T")

    S = st.slider("Spot",100,1000,500)
    r = st.slider("Interest %",0,15,8)/100
    c = st.slider("Dividend %",0,10,2)/100
    T = st.slider("Time",0.1,1.0,0.5)

    F = S*(1+r-c)**T
    st.metric("Futures price", round(F,2))

# =====================================================
# 3 MTM
# =====================================================
elif topic == "3. MTM & Margins":
    st.header("Mark-to-Market")

    entry = st.number_input("Entry price",22000)
    price = st.slider("Current price",18000,26000,22100)
    contracts = st.slider("Contracts",1,50,5)

    pnl = (price-entry)*contracts*50
    st.metric("Daily P&L", f"₹{pnl:,.0f}")

# =====================================================
# 4 TRADING PNL
# =====================================================
elif topic == "4. Trading P&L":
    st.header("Long vs Short")

    entry = st.number_input("Entry",22000)
    price = st.slider("Price",18000,26000,22000)
    contracts = st.slider("Contracts",1,50,5)

    long = (price-entry)*contracts*50
    short = (entry-price)*contracts*50

    c1,c2 = st.columns(2)
    c1.metric("Long",f"₹{long:,.0f}")
    c2.metric("Short",f"₹{short:,.0f}")

# =====================================================
# 5 TRADING BUILDER
# =====================================================
elif topic == "5. Trading Strategy Builder":
    st.header("Directional Strategy")

    entry = st.number_input("Entry price",22000)
    contracts = st.slider("Contracts",1,20,5)

    prices = np.linspace(18000,26000,100)
    pnl = (prices-entry)*contracts*50

    fig, ax = plt.subplots()
    ax.plot(prices,pnl)
    ax.axhline(0)
    st.pyplot(fig)

# =====================================================
# 6 HEDGING BUILDER
# =====================================================
elif topic == "6. Hedging Strategy Builder":
    st.header("Portfolio Hedging")

    V = st.number_input("Portfolio value",5000000)
    beta = st.slider("Beta",0.5,1.5,1.0)
    contracts = st.slider("Contracts",0,100,20)
    F = st.number_input("Futures price",22000)

    moves = np.linspace(-0.1,0.1,100)

    port = V*beta*moves
    fut = -contracts*50*F*moves
    net = port+fut

    fig, ax = plt.subplots()
    ax.plot(moves*100,port,label="Portfolio")
    ax.plot(moves*100,net,label="Hedged")
    ax.legend()
    st.pyplot(fig)

# =====================================================
# 7 OPTIMAL HEDGE
# =====================================================
elif topic == "7. Optimal Hedge Ratio":
    st.header("Optimal Hedge Ratio")

    V = st.number_input("Portfolio",5000000)
    beta = st.slider("Beta",0.5,1.5,1.0)
    F = st.number_input("Futures price",22000)

    correct = (beta*V)/(F*50)
    st.metric("Optimal contracts",round(correct,2))

# =====================================================
# 8 BASIS
# =====================================================
elif topic == "8. Basis & Convergence":
    st.header("Basis")

    spot = st.number_input("Spot",22000)
    futures = st.number_input("Futures",22100)

    st.metric("Basis",spot-futures)
    st.write("At expiry → basis → 0")

# =====================================================
# 9 BASIS RISK
# =====================================================
elif topic == "9. Basis Risk":
    st.header("Basis Risk")

    corr = st.slider("Correlation",0.0,1.0,0.8)
    st.metric("Hedge effectiveness",round(corr*100,1))

# =====================================================
# 10 ROLLING
# =====================================================
elif topic == "10. Rolling Futures":
    st.header("Rolling Futures")

    near = st.number_input("Near contract",22000)
    far = st.number_input("Next contract",22150)

    st.metric("Roll cost",far-near)

# =====================================================
# 11 MATCHING
# =====================================================
elif topic == "11. Matching System":
    st.header("Exchange Matching")

    buyers = st.slider("Buy orders",0,100,60)
    sellers = st.slider("Sell orders",0,100,50)

    st.metric("Trades executed",min(buyers,sellers))

# =====================================================
# 12 CASES
# =====================================================
elif topic == "12. Real-World Cases":

    st.header("Case Practice")

    case = st.selectbox(
        "Select Case",
        ["Equity Portfolio Hedge","Airline Fuel Hedge","Exporter Hedge"]
    )

    if case=="Equity Portfolio Hedge":
        st.write("₹5Cr portfolio, futures 22000, size 50")
        ans = st.number_input("Contracts?")
        correct = (5_000_000)/(22000*50)
        if st.button("Check"):
            st.write(f"Optimal ≈ {round(correct,1)}")

    elif case=="Airline Fuel Hedge":
        st.write("Fuel exposure, corr=0.8")
        choice = st.radio("Decision",["Full","Partial","None"])
        if st.button("Check"):
            st.write("Best: Partial hedge")

    else:
        st.write("Exporter receives USD")
        choice = st.radio("Decision",["Long USD","Short USD"])
        if st.button("Check"):
            st.write("Correct: Short USD futures")

# =====================================================
# 13 ADVANCED STRATEGIES
# =====================================================
elif topic == "13. Advanced Strategies":

    st.header("Advanced Strategies")

    strat = st.selectbox(
        "Strategy",
        [
            "Directional Trade",
            "Calendar Spread",
            "Cash-and-Carry Arbitrage",
            "Reverse Arbitrage",
            "Basis Trade",
            "Roll-Over Strategy",
            "Partial Hedge",
            "Over Hedge"
        ]
    )

    if strat=="Directional Trade":
        entry = st.number_input("Entry",22000)
        contracts = st.slider("Contracts",1,20,5)
        prices = np.linspace(18000,26000,100)
        pnl = (prices-entry)*contracts*50
        fig, ax = plt.subplots()
        ax.plot(prices,pnl)
        ax.axhline(0)
        st.pyplot(fig)

    elif strat=="Calendar Spread":
        near = st.number_input("Near",22000)
        far = st.number_input("Far",22200)
        st.metric("Spread",far-near)

    elif strat=="Cash-and-Carry Arbitrage":
        spot = st.number_input("Spot",1000)
        fut = st.number_input("Futures",1050)
        r = st.slider("Rate",0,15,8)/100
        fair = spot*(1+r)
        st.metric("Fair value",round(fair,2))

    elif strat=="Reverse Arbitrage":
        st.write("When futures below fair value → sell spot buy futures")

    elif strat=="Basis Trade":
        spot = st.number_input("Spot",22000)
        fut = st.number_input("Futures",22100)
        st.metric("Basis",spot-fut)

    elif strat=="Roll-Over Strategy":
        near = st.number_input("Near",22000)
        nxt = st.number_input("Next",22150)
        st.metric("Roll cost",nxt-near)

    elif strat=="Partial Hedge":
        V = st.number_input("Portfolio",5000000)
        pct = st.slider("Hedge %",0,100,50)
        st.metric("Hedged value",V*pct/100)

    else:
        st.write("Too many futures → speculative risk")

# =====================================================
# 14 QUIZ + CERTIFICATE
# =====================================================
elif topic == "14. Quiz & Certificate":

    st.header("Futures Quiz")

    score = 0

    q1 = st.radio("1. Market falls → who gains?",["Long","Short"])
    q2 = st.radio("2. Basis at expiry?",["Zero","Large"])
    q3 = st.number_input("3. Spot100 r10% futures?")
    q4 = st.number_input("4. Buy200→210 size50 P&L?")
    q5 = st.number_input("5. Hedge contracts ₹10L?")
    q6 = st.radio("6. MTM reduces?",["Credit risk","Return"])
    q7 = st.radio("7. Futures>spot?",["Contango","Backwardation"])
    q8 = st.radio("8. Best hedge corr?",["High","Low"])
    q9 = st.radio("9. Rolling means?",["Close & reopen","Hold"])
    q10 = st.number_input("10. Short500→520 size10 loss?")

    if st.button("Submit Quiz"):

        if q1=="Short": score+=1
        if q2=="Zero": score+=1
        if abs(q3-110)<1: score+=1
        if abs(q4-500)<1: score+=1
        if abs(q5-1)<0.5: score+=1
        if q6=="Credit risk": score+=1
        if q7=="Contango": score+=1
        if q8=="High": score+=1
        if q9=="Close & reopen": score+=1
        if abs(q10-200)<1: score+=1

        st.success(f"Score {score}/10")

        if score >= 5:
            name = st.text_input("Enter name for certificate")

            if name:
                buffer = io.BytesIO()
                c = canvas.Canvas(buffer, pagesize=letter)
                width, height = letter

                c.setStrokeColor(HexColor("#C9A227"))
                c.setLineWidth(4)
                c.rect(30,30,width-60,height-60)

                c.setFont("Helvetica-Bold",28)
                c.drawCentredString(width/2,height-140,
                                    "Certificate of Completion")

                c.setFont("Helvetica",16)
                c.drawCentredString(width/2,height-180,
                                    "Futures Trading Lab")

                c.setFont("Helvetica-Bold",24)
                c.drawCentredString(width/2,height-240,name)

                c.drawCentredString(width/2,height-280,
                                    f"Score: {score}/10")

                today = datetime.today().strftime("%d %B %Y")
                c.drawCentredString(width/2,height-320,today)

                c.drawCentredString(width/2,height-360,
                                    "Instructor: Prof. Shalini Velappan")

                c.save()
                buffer.seek(0)

                st.download_button(
                    "Download Certificate",
                    buffer,
                    file_name="certificate.pdf"
                )
