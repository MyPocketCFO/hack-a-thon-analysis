import matplotlib.pyplot as plt
import seaborn as sns

def plot_metrics(main_company, competitors):
    # Example: Plot Gross Margin comparison
    plt.figure(figsize=(10, 6))
    sns.barplot(x=['Main Company', 'Competitor 1', 'Competitor 2', 'Competitor 3', 'Competitor 4', 'Competitor 5'],
                y=[main_company['Gross Margin'].mean()] + [comp['Gross Margin'].mean() for comp in competitors])
    plt.title('Gross Margin Comparison')
    plt.ylabel('Gross Margin (%)')
    plt.show()

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    # Example: Plot Net Profit Margin comparison
    plt.figure(figsize=(10, 6))
    sns.barplot(x=['Main Company', 'Competitor 1', 'Competitor 2', 'Competitor 3', 'Competitor 4', 'Competitor 5'],
                y=[main_company['Net Profit Margin'].mean()] + [comp['Net Profit Margin'].mean() for comp in competitors])
    plt.title('Net Profit Margin Comparison')
    plt.ylabel('Net Profit Margin (%)')
    plt.show()

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
if __name__ == "__main__":
    from data_processing import main
    main_company, competitors = main()
    plot_metrics(main_company, competitors)