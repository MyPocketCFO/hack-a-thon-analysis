from scripts.data_processing import main as load_data
from scripts.analysis import generate_analysis_report
from scripts.visualization import plot_metrics
from scripts.chatbot import generate_chatbot_response

def main():
    # Load and preprocess data
    main_company, competitors = load_data()
    
    # Generate analysis report
    report = generate_analysis_report(main_company, competitors)
    
    # Visualize metrics
    plot_metrics(main_company, competitors)
    
    # Generate chatbot response
    chatbot_response = generate_chatbot_response(report)
    print(chatbot_response)

if __name__ == "__main__":
    main()