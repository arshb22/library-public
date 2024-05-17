import matplotlib.pyplot as plt

class SblDomain:
    def __init__(self, df):
        self.df = df

    def visualize_loan_amount(self):
        self.df['loan_amount'].hist()
        plt.title('SBL Data')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()