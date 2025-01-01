#!/bin/sh

echo "Running Streamlit app"
streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --browser.serverAddress=$SERVER_ADDRESS
