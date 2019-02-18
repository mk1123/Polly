Polli
=====
##Jason Chang and Manan Khattar<br/> 2019.02.15 - 02.17 @TreeHacks 2019

#### Proposed Question: <br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*An intelligent political bot for electoral awareness.*

## Inspiration

####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The 2016 United States presidential election is one of the most contentious president election in the history of American politics. The US government publicly announced that it was "confident" Russia orchestrated the hacking of the Democratic National Committee and other political organizations of the Democratic Party. Those hacks resulted in the public release of thousands of stolen emails, many of which included damaging revelations about the Democratic Party and former Secretary of State Hillary Clinton, the party's nominee. As a team at Polli, we believe such vulnerability of American politics was exposed mainly due to the Americans’ lack of awareness, understanding, and trust in the U.S. electoral system. Inspired by Resistbot that helps voters to contact their officials, we designed Polli, an intelligent political bot for electoral awareness.


## What it does?

####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Based on the user’s response from a brief conversation with Polli, our web application provides personalized, tailor-made analytical information about incoming elections based on the user’s location.

## How we built it?

####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Due to the current uncertainty of dimensionality in the realm of linguistics, we were unsure of the optimal algorithmic approach to perform the classification on natural language processing input tokens. To reduce the complexity of the input data, we tokenize complex sentence structure into list of individual words to inspect independent sentimental polarity. Due to the uncertainty in best choice of classifier, we established an aggregated voting system of seven classifier, three Naive Bayes classifiers (Original, Multinomial, Bernoulli) and four other non-Bayesian approach classifiers (Logistic Regression, Stochastic Gradient Descent, Linear Support Vector Classification, Nu-Support Vector Classification). Since the output label is binary, +1 for positive sentiment and -1 for negative sentiment, we aggregated outputs from all seven classifiers by summing up the outputs and taking the sign of that value for conclusive label. Combined, seven classifiers showed a mean accuracy of 75%.

####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Once we processed all the textual political information, we used Flask and Dialogflow to connect our backend and frontend together. Dialogflow contained the bulk of our conversational logic, and we handled variable state, contextual information and further data processing using our Data model in Flask. We connected our Wix Code website to our Flask backend as well. 

## Aggregated Classifiers
####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; We took a simple majority vote out of all the different classifiers that we use. Because this is a binary classification problem and because we intentionally used an odd number of classifiers, there is no possibility of a tie. The input sentence is classified to contain an positive (or negative) opinion based upon whichever class secures the majority vote.

## Challenges We Ran Into

####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Due to the inconsistency in formatting of various political forums, it was challenging to approach data mining by web scraping to collect large amount of historical electoral data. In addition, it was quite difficult to encode the looping and variable conversational flow logic we needed in Dialogflow, especially since we wanted to integrate Facebook Messenger’s quick replies. 

## Accomplishments that We're proud of

####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; With the technique of massive web scraping and crawling, we were able to manually extract more than 75,000 records of historical electoral data dated all the way back to the year of 2000 from scratch. We were able to train an ensemble classifier that label our datasets in terms of sentiment analysis with an accuracy of 75%.

## What We've learned

####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Mainly, we practiced developing chatbot logic by working with Dialogflow conversational design platform. From our experience, although such agent is equipped with precise natural language processing (NLP) capability, we have identified such inferiority of the platform in terms of processing logic control flow, which we have decided to implement in the Python Flask back-end framework instead. Additionally, it was fascinating to witness the enormous machinery of politics working as an entity under the U.S. electoral system.

## What's next for Polli

####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The next step for Polli would be to implement a more interactive dynamic design for the front-end development of the web application. In addition, we would want to expand the magnitude of our training dataset in terms of time serialization to perhaps more than 30 years back (1990s) to better understand the trend of the American electoral system and amplify the power of Polli to analyze opinions of various politicians.

##Built With
####GCP •	Dialogflow •	Flask •	Python •	Wix Code •	ngrok •	Tensorflow • Adobe Illustrator • Beautiful Soup

##Try it out
####[GitHub Repo](https://github.com/mk1123/Polly)

##Demo
####[Link](https://www.youtube.com/watch?v=6TU2SVUtFfY&list=UUwP32fqS-9Frxl0mtjQ4JlQ&index=2)

##Snapshots
![Fig.1] (https://d.pr/i/tbkyk3)
![Fig.2] (https://d.pr/i/bSZV1A)
![Fig.3] (https://d.pr/i/UvY9uy)
![Fig.4] (https://d.pr/i/miXcoH)
![Fig.5] (https://d.pr/i/2DPheo)
![Fig.6] (https://d.pr/i/YHq1mO)


