import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def model(input1, input2):
    x = np.arange(0, 10, 0.1)
    y = input1 * np.sin(x + input2)
    df = pd.DataFrame({'x': x, 'y': y})
    return df

def main():
    st.title("Data Visualization App")

    # Define sliders for model inputs, need to switch this to a format that fits the model input
    input1 = st.slider("Input 1", min_value=1, max_value=10, value=5)
    input2 = st.slider("Input 2", min_value=0, max_value=10, value=1)

    # Generate DataFrame based on model function
    df = model(input1, input2)

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(df['x'], df['y'])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Plot of y vs. x')

    # Display the plot in the Streamlit app
    st.pyplot(fig)

if __name__ == "__main__":
    main()
