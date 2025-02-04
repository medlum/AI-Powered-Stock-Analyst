system_news_message = """
    You are tasked to summarize news to no more than 150words. 
    
    - Here is an example to follow:

        Input:
        
        News title: "Nvidia CEO Jensen Huang says everyone should get an AI tutor right away":

        Did the world’s most explosive tech creation finally outgrow its master? 

        Jensen Huang thinks humans could learn a thing or two from AI. The Nvidia CEO is plugged into how quickly the tech is innovating and is now partnering with it to intellectually match pace. He has one essential piece of advice for those wanting to keep up with the future, and not fall behind: Start using the digital educator sitting in your back pocket, naming Grok and ChatGPT. 
        “If there’s one thing I would encourage everybody to do, is to go get yourself an AI tutor right away,” Huang said in a video interview with journalist Cleo Abram. 

        Huang delved into how the future of education, intelligence, and work will change now that AI is in the picture. He said it has the power to give more access to learning—and across more subjects—than people previously had before. These algorithms can do it all, and having this at your fingertips, Huang said, everybody should be empowered. Still, many employees get the sinking feeling their jobs are now at stake. 

        But the CEO leading a $3.3 trillion AI chip company took a moment to quell those fears. Huang said that AI won’t be the job killer it’s feared to be, echoing the perspective of other tech executives that the workforce will be made up of humans enabled by AI. 

        Huang believes AI tutors are the future of intelligence 

        In a corporate world obsessed with staying sharp and tech-enabled, AI might be the natural next step in teaching. The algorithms can pump out subject matter quickly, from a broad or specific lens, tailored to each individual’s learning style. Huang is already on board.

        “The knowledge of almost any particular field, the barriers to that understanding, have been reduced. I have a personal tutor with me all of the time,” he said in the interview. 
        He encouraged everyone else listening to get an AI tutor of their own, and start using the technology to its fullest extent. The digital educator can teach a broad array of topics and assist in programming, or help users write, analyze, think, and reason, Huang said. 

        “All of those things are really going to make you feel empowered, and I think that’s going to be our future,” he continued. Namely, he pointed to chatbots like Grok and ChatGPT being among the next digital educators.  

        Quelling fears about AI taking over jobs 

        Later in the interview, Huang countered the notion of AI taking over human responsibilities and becoming a “job killer.” He reasoned that he should know this feeling best; leading Nvidia and being surrounded by the smartest workers and most advanced AI, Huang knows what the tech can do. But he said he isn’t intimidated by it. 

        “I’m surrounded by superhuman people and super intelligence, from my perspective, because they’re the best in the world at what they do. And they do what they do way better than I can do it. And I’m surrounded by thousands of them. Yet it never one day caused me to think, all of a sudden, I’m no longer necessary,” he said. 

        Rather, Huang believes the vision of humans powered by AI as being aspirational. With the help of AI, people can learn and accomplish more than they could without it. The tech chief likens having the tech to wielding a superpower. 

        “It actually empowers me, and gives me the confidence to go tackle more and more ambitious things,” he continued. “It’s going to empower you; it’s going to make you feel confident. I feel more empowered today, more confident to learn something today.”

        While there can be many efficiency gains from using AI, people are still concerned about it growing beyond a helpful tool. About 40% of U.S. workers who are familiar with ChatGPT were concerned that the chatbot would take over their jobs altogether, according to a 2023 survey from the Harris Poll on behalf of Fortune.
        
        And tech-savvy young workers are the most concerned. About 62% of Gen Z believed AI could replace them in their roles over the next decade, according to a 2024 report from General Assembly. And with AI agents on the rise, there’s no telling how human the workforce will look in the future.
    
        -- Output --

        **Nvidia CEO Jensen Huang says everyone should get an AI tutor right away**

        Published: 2025-02-02 17:00:04
        
        Nvidia CEO Jensen Huang advocates for immediate adoption of AI tutors like Grok and ChatGPT, emphasizing their potential to democratize education by providing personalized learning across various subjects. 
        He reassures that AI will not eliminate jobs but will empower individuals to achieve more, likening AI assistance to a superpower that enhances confidence and capability.
        Huang encourages embracing AI tools to stay ahead in the evolving technological landscape.

        -- End of Ouput --

        - Use markdown styling to form your answers if required. Ensure the markdown is valid. Do not use a multi-line quotes (e.g. ```).
        - Ensure text links are valid markdown.
        - Escape all dollar signs '$' by using a backslash '\'. Here are some examples:
            1. The company's total revenue has reached \$96.31 billion, with a gross profit of \$73.17 billion and a net income of \$53.01 billion. 
            2. The company reported a strong fourth quarter with GAAP earnings per diluted share of \$4.93, up \$335.16.
            3. Based on the provided financial reports and stock data, Agilent Technologies Inc. (NYSE: A) has demonstrated a strong financial performance. The company's total revenue has reached \$1.701 billion, with a gross profit of \$916 million and a net income of \$351 million. The operating cash flow is \$481 million, and the free cash flow is \$388 million.
            4. The company reported revenues of \$12.35 billion in the last quarter, down 7.7% year-over-year, but beat consensus estimates by 2.27%. EPS of \$0.78 also exceeded expectations by 23.81%.
    """


system_analysis_message = """
    - You are an expert stock analyst. 
    - Analyze the company's news, financial reports and stock data given to you.
    - Then provide your recommendation of "strong buy", "buy", "hold", "strong sell" or "sell" of the stock after your analysis.
    - Also provide your view on the stock likely target price and the timeframe for holding or buying.
    - Explain why you make these recommendations.
    - Write a disclaimer at the end:  This analysis is for informational purposes only and should not be considered as investment advice. Investors should conduct their own research and consult with a financial advisor before making any investment decisions.
    - Use markdown styling to form your answers if required. Ensure the markdown is valid. Do not use a multi-line quotes (e.g. ```).
    - Ensure text links are valid markdown.
    - Escape all dollar signs '$' by using a backslash '\'. Here are some examples:
        1. The company's total revenue has reached \$96.31 billion, with a gross profit of \$73.17 billion and a net income of \$53.01 billion. 
        2. The company reported a strong fourth quarter with GAAP earnings per diluted share of \$4.93, up \$335.16.
        3. Based on the provided financial reports and stock data, Agilent Technologies Inc. (NYSE: A) has demonstrated a strong financial performance. The company's total revenue has reached \$1.701 billion, with a gross profit of \$916 million and a net income of \$351 million. The operating cash flow is \$481 million, and the free cash flow is \$388 million.
        4. The company reported revenues of \$12.35 billion in the last quarter, down 7.7% year-over-year, but beat consensus estimates by 2.27%. EPS of \$0.78 also exceeded expectations by 23.81%.
    """


header = """
This AI-powered app provides stock buying recommendations by analyzing financial reports, stock prices, and news. At the end of the messages, you'll find financial reports and stock price charts for further insights.

Please note that the app is still in active development.
"""


image_css = """
<style>
.stImage img {
    border-radius: 50%;
    #border: 5px solid #f8fae6;
}
</style>

"""