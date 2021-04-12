// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
//
// Generated with Bot Builder V4 SDK Template for Visual Studio EchoBot v4.12.2

using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace CyclingBot.Bots
{
    public class EchoBot : ActivityHandler
    {
        protected override async Task OnMessageActivityAsync(ITurnContext<IMessageActivity> turnContext, CancellationToken cancellationToken)
        {
            dynamic value = turnContext.Activity.Value;

            if (value == null)
            {
                string adaptiveCardPath = Path.Combine(".", "Resources", "WorkoutTemplate.json");
                var cardAttachment = CreateAdaptiveCardAttachment(adaptiveCardPath);
                await turnContext.SendActivityAsync(MessageFactory.Attachment(cardAttachment), cancellationToken);
                await turnContext.SendActivityAsync(MessageFactory.Text("Please submit for your workout prediction."), cancellationToken);
            }
            else
            {

                // Test Print for Teams output
                //await turnContext.SendActivityAsync(MessageFactory.Text(value.ToString(), value.ToString()), cancellationToken);

                // Retrieve the data from fields
                string cardCity = value.cityInput;
                string cardDate = value.dateInput;
                string cardTime = value.timeInput;

                // Test Print for Teams output
                //await turnContext.SendActivityAsync(MessageFactory.Text(cardCity+ cardDate + cardTime, cardCity + cardDate + cardTime), cancellationToken);

                string result = await PredictWorkout(cardCity, cardDate, cardTime);

                //Post the API response to bot again
                await turnContext.SendActivityAsync(MessageFactory.Text(result, result), cancellationToken);
            }
        }

        async private Task<String> PredictWorkout(string wCity, string wDate, string wTime)
        {
            try
            {
                using (HttpClient client = new HttpClient())
                {
                    //Assuming that the api takes the user message as a query paramater
                    string RequestURI = String.Format("https://datadrivencycling.azurewebsites.net/predict?city={0}&date={1}&time={2}",wCity,wDate,wTime);
                    HttpResponseMessage responsemMsg = await client.GetAsync(RequestURI);
                    string apiResponse = "";
                    if (responsemMsg.IsSuccessStatusCode)
                    {
                        apiResponse = await responsemMsg.Content.ReadAsStringAsync();
                    }

                    return apiResponse;
                }
            }
            catch (Exception ex)
            {
                return ex.ToString();
            }
        }

        private static Attachment CreateAdaptiveCardAttachment(string filePath)
        {
            var adaptiveCardJson = File.ReadAllText(filePath);
            var adaptiveCardAttachment = new Attachment()
            {
                ContentType = "application/vnd.microsoft.card.adaptive",
                Content = JsonConvert.DeserializeObject(adaptiveCardJson),
            };
            return adaptiveCardAttachment;
        }

        protected override async Task OnMembersAddedAsync(IList<ChannelAccount> membersAdded, ITurnContext<IConversationUpdateActivity> turnContext, CancellationToken cancellationToken)
        {
            var welcomeText = "Hello and welcome!";
            foreach (var member in membersAdded)
            {
                if (member.Id != turnContext.Activity.Recipient.Id)
                {
                    await turnContext.SendActivityAsync(MessageFactory.Text(welcomeText, welcomeText), cancellationToken);
                }
            }
        }
    }
}
