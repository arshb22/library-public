import matplotlib.pyplot as plt

class BankingDomain:
    def __init__(self, df):
        self.df = df

    def visualize_balance_distribution(self):
        self.df['balance'].hist()
        plt.title('Banking Data')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()
