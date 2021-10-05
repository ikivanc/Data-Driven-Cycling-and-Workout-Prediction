// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
//

using CyclingPrediction.Models;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace CyclingPrediction.Bots
{
    public class CyclingBot : ActivityHandler
    {
        protected override async Task OnMessageActivityAsync(ITurnContext<IMessageActivity> turnContext, CancellationToken cancellationToken)
        {
            dynamic value = turnContext.Activity.Value;

            if (value == null){
                string adaptiveCardPath = Path.Combine(".", "Resources", "WorkoutTemplate.json");
                var cardAttachment = CreateAdaptiveCardAttachment(adaptiveCardPath);
                await turnContext.SendActivityAsync(MessageFactory.Attachment(cardAttachment), cancellationToken);
            }
            else{
                // Test Print for Teams output
                //await turnContext.SendActivityAsync(MessageFactory.Text(value.ToString(), value.ToString()), cancellationToken);

                // Retrieve the data from fields
                string cardCity = value.cityInput;
                string cardDate = value.dateInput;
                string cardTime = value.timeInput;

                // Test Print for Teams output
                //await turnContext.SendActivityAsync(MessageFactory.Text(cardCity+ cardDate + cardTime, cardCity + cardDate + cardTime), cancellationToken);

                // TODO
                // Control inputs incase MSTeams mobile or other apps send empty inputs.
                if(!String.IsNullOrEmpty(cardCity) && !String.IsNullOrEmpty(cardDate) && !String.IsNullOrEmpty(cardTime))
                {
                    WorkoutPrediction result = await PredictWorkout(cardCity, cardDate, cardTime);
                    
                    if (result.Error == null){
                        Attachment attachment = GetThumbnailCard(result);
                        //Post the API response to bot again
                        await turnContext.SendActivityAsync(MessageFactory.Attachment(attachment), cancellationToken);
                    }
                    else{
                        string errorMessage = "An error occured: " + result.Error;
                        await turnContext.SendActivityAsync(MessageFactory.Text(errorMessage, errorMessage), cancellationToken);
                    }
                }
                else{
                    string errorMessage = "Invalid Input, Please make sure, you have correct inputs";
                    await turnContext.SendActivityAsync(MessageFactory.Text(errorMessage, errorMessage), cancellationToken);
                }
            }
        }

        private static Attachment GetThumbnailCard(WorkoutPrediction wprediction)
        {
            var thumbnailCard = new ThumbnailCard
            {
                Title = String.Format("{0}, mininum {1}km", wprediction.Ride, wprediction.Distance),
                Subtitle = wprediction.Weather,
                Text = String.Format("Weather details: Temperature: {0}C, Wind: {1}", wprediction.Temp, wprediction.Wind),
                Images = new List<CardImage> { new CardImage(wprediction.WeatherIcon) }
            };

            return thumbnailCard.ToAttachment();
        }

        async private Task<WorkoutPrediction> PredictWorkout(string wCity, string wDate, string wTime)
        {
            try{
                using (HttpClient client = new HttpClient()){
                    //Assuming that the api takes the user message as a query paramater
                    string RequestURI = String.Format("https://{your-cycling-bot-endpoint}.azurewebsites.net/predict?city={0}&date={1}&time={2}",wCity,wDate,wTime);
                    HttpResponseMessage responsemMsg = await client.GetAsync(RequestURI);
                    WorkoutPrediction predictionResult = new WorkoutPrediction();
                    if (responsemMsg.IsSuccessStatusCode){
                        string apiResponse = await responsemMsg.Content.ReadAsStringAsync();

                        predictionResult = JsonConvert.DeserializeObject<WorkoutPrediction>(apiResponse);
                    }
                    return predictionResult;
                }
            }
            catch (Exception ex){
                WorkoutPrediction predictionResult = new WorkoutPrediction();
                predictionResult.Error = ex.ToString();
                return predictionResult;
            }
        }

        private static Attachment CreateAdaptiveCardAttachment(string filePath)
        {
            var adaptiveCardJson = File.ReadAllText(filePath);
            var adaptiveCardAttachment = new Attachment(){
                ContentType = "application/vnd.microsoft.card.adaptive",
                Content = JsonConvert.DeserializeObject(adaptiveCardJson),
            };
            return adaptiveCardAttachment;
        }

        protected override async Task OnMembersAddedAsync(IList<ChannelAccount> membersAdded, ITurnContext<IConversationUpdateActivity> turnContext, CancellationToken cancellationToken)
        {
            var welcomeText = "Welcome to your personal Cycling Prediction. Please submit for your workout prediction!";
            foreach (var member in membersAdded){
                if (member.Id != turnContext.Activity.Recipient.Id){
                    await turnContext.SendActivityAsync(MessageFactory.Text(welcomeText, welcomeText), cancellationToken);
                }
            }
        }
    }
}
