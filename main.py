import streamlit as st
from bsedata.bse import BSE
import yfinance as yf
import matplotlib.pyplot as plt
from config import start_date
from datetime import datetime

# Define the list of stock codes and their names
stock_data = {
    '500002': 'ABB India Limited',
    '539254': 'Adani Energy Solutions Ltd',
    '512599': 'ADANI ENTERPRISES LTD.',
    '541450': 'Adani Green Energy Ltd',
    '532921': 'ADANI PORTS AND SPECIAL ECONOMIC ZONE LTD.',
    '533096': 'ADANI POWER LTD.',
    '542066': 'Adani Total Gas Ltd',
    '500425': 'AMBUJA CEMENTS LTD.',
    '508869': 'APOLLO HOSPITALS ENTERPRISE LTD.',
    '500820': 'ASIAN PAINTS LTD.',
    '540376': 'Avenue Supermarts Ltd',
    '532215': 'AXIS BANK LTD.',
    '532977': 'BAJAJ AUTO LTD.',
    '500034': 'Bajaj Finance Limited',
    '532978': 'BAJAJ FINSERV LTD.',
    '500490': 'BAJAJ HOLDINGS & INVESTMENT LTD.',
    '532134': 'BANK OF BARODA',
    '509480': 'BERGER PAINTS INDIA LTD.',
    '500049': 'BHARAT ELECTRONICS LTD.',
    '500547': 'BHARAT PETROLEUM CORPORATION LTD.',
    '532454': 'BHARTI AIRTEL LTD.',
    '500825': 'BRITANNIA INDUSTRIES LTD.',
    '500093': 'CG Power and Industrial Solutions Ltd',
    '511243': 'Cholamandalam Investment and Finance Company Ltd',
    '500087': 'CIPLA LTD.',
    '533278': 'COAL INDIA LTD.',
    '500096': 'DABUR INDIA LTD.',
    '532488': "DIVI'S LABORATORIES LTD.",
    '532868': 'DLF LTD.',
    '500124': "DR.REDDY'S LABORATORIES LTD.",
    '505200': 'EICHER MOTORS LTD.',
    '532155': 'GAIL (INDIA) LTD.',
    '532424': 'GODREJ CONSUMER PRODUCTS LTD.',
    '500300': 'GRASIM INDUSTRIES LTD.',
    '517354': 'HAVELLS INDIA LTD.',
    '532281': 'HCL TECHNOLOGIES LTD.',
    '500180': 'HDFC Bank Ltd',
    '500440': 'HINDALCO INDUSTRIES LTD.',
    '541154': 'Hindustan Aeronautics Ltd',
    '500696': 'HINDUSTAN UNILEVER LTD.',
    '500188': 'HINDUSTAN ZINC LTD.',
    '532174': 'ICICI BANK LTD.',
    '540716': 'ICICI Lombard General Insurance Company Ltd',
    '540133': 'ICICI Prudential Life Insurance Company Ltd',
    '500116': 'IDBI BANK LTD.',
    '530965': 'INDIAN OIL CORPORATION LTD.',
    '532388': 'INDIAN OVERSEAS BANK',
    '543257': 'Indian Railway Finance Corporation Ltd',
    '532187': 'INDUSIND BANK LTD.',
    '500209': 'INFOSYS LTD.',
    '539448': 'InterGlobe Aviation Ltd',
    '500875': 'ITC LTD.',
    '532286': 'JINDAL STEEL & POWER LTD.',
    '543940': 'Jio Financial Services Ltd',
    '533148': 'JSW Energy Ltd',
    '500228': 'JSW STEEL LTD.',
    '500247': 'KOTAK MAHINDRA BANK LTD.',
    '500510': 'LARSEN & TOUBRO LTD.',
    '543526': 'Life Insurance Corporation of India',
    '540005': 'LTI Mindtree Ltd',
    '543287': 'Macrotech Developers Ltd',
    '500520': 'MAHINDRA & MAHINDRA LTD.',
    '543904': 'Mankind Pharma Ltd',
    '531642': 'MARICO LTD.',
    '532500': 'MARUTI SUZUKI INDIA LTD.',
    '500790': 'NESTLE INDIA LTD.',
    '532555': 'NTPC LTD.',
    '500312': 'Oil and Natural Gas Corporation Ltd',
    '500331': 'PIDILITE INDUSTRIES LTD.',
    '542652': 'Polycab India Ltd',
    '532810': 'POWER FINANCE CORPORATION LTD.',
    '532898': 'POWER GRID CORPORATION OF INDIA LTD.',
    '532461': 'PUNJAB NATIONAL BANK',
    '500325': 'RELIANCE INDUSTRIES LTD.',
    '517334': 'Samvardhana Motherson International Ltd',
    '543066': 'SBI Cards and Payment Services Ltd',
    '540719': 'SBI Life Insurance Company Ltd',
    '500387': 'SHREE CEMENT LTD.',
    '511218': 'Shriram Finance Ltd',
    '500550': 'SIEMENS LTD.',
    '503806': 'SRF LTD.',
    '500112': 'STATE BANK OF INDIA',
    '524715': 'SUN PHARMACEUTICAL INDUSTRIES LTD.',
    '532540': 'TATA CONSULTANCY SERVICES LTD.',
    '500800': 'Tata Consumer Products Ltd',
    '500570': 'TATA MOTORS LTD.',
    '500400': 'TATA POWER CO.LTD.',
    '500470': 'TATA STEEL LTD.',
    '532755': 'TECH MAHINDRA LTD.',
    '500114': 'Titan Company Limited',
    '500251': 'TRENT LTD.',
    '532343': 'TVS MOTOR COMPANY LTD.',
    '532538': 'ULTRATECH CEMENT LTD.',
    '532477': 'UNION BANK OF INDIA',
    '532432': 'UNITED SPIRITS LTD.',
    '540180': 'Varun Beverages Ltd',
    '500295': 'Vedanta Limited',
    '507685': 'WIPRO LTD.',
    '543320': 'Zomato Ltd',
    '540777': 'HDFC Life Insurance Company Ltd',
}

# Title for your Streamlit app
# Extract the stock codes and stock names as separate lists
stock_codes = list(stock_data.keys())
stock_names = list(stock_data.values())

# Set Streamlit App Title and Page Icon
st.set_page_config(
    page_title="Financial Stock Viewer",
    page_icon="💹",
)

# Create a custom Streamlit theme
st.markdown(
    """
    <style>
    .st-d6 {
        background-color: #f0f8ff;
        color: #000000;
    }
    .st-ba {
        font-size: 18px;
    }
    .st-bu {
        font-size: 16px;
    }
    .st-br {
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
    }
    .st-dg {
        font-size: 24px;
        color: #000000;
        background-color: #f0f8ff;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title for your Streamlit app
st.title('Financial Stock Viewer')

# Sidebar with user input
st.sidebar.header('User Input')

# Dropdown for stock code and name selection
st.sidebar.subheader('Select Stock')
selected_stock = st.sidebar.selectbox('Choose a stock', list(zip(stock_codes, stock_names)))

# Separate the selected option into code and name
selected_stock_code, selected_stock_name = selected_stock

# Text input for start date
st.sidebar.subheader('Start Date (YYYY-MM-DD)')
user_start_date = st.sidebar.text_input('Enter start date', start_date)

# Convert user input start date to datetime
try:
    user_start_date = datetime.strptime(user_start_date, '%Y-%m-%d').date()
except ValueError:
    st.error("Please enter a valid date in the format YYYY-MM-DD.")
    st.stop()

# Create a BSE instance
b = BSE()

# Get the securityID of the selected stock
security_id = b.getQuote(selected_stock_code)['securityID']

# Convert in the format of 'securityID.NS' for Yahoo Finance
data = [security_id + '.NS']

# Download the data from Yahoo Finance from user-selected start date
frame = yf.download(data, start=user_start_date)

# Filter the data to get only the prices
closes = frame['Adj Close']

# Display the selected stock code and name
st.markdown(f'<div class="st-dg">Stock: {selected_stock_name} ({selected_stock_code})</div>', unsafe_allow_html=True)

# Display the stock price data
st.header('Stock Price Data')
st.dataframe(closes)

# Plotting the graph using matplotlib pyplot
st.header('Stock Price Chart')
grph = closes.plot(kind='line', lw=1, title=f'Stock prices for {selected_stock_name}', figsize=(12, 8))
st.pyplot(plt)
