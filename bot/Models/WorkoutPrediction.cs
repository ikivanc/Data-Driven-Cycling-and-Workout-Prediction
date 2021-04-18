using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace CyclingPrediction.Models
{
    public class WorkoutPrediction
    {
        public int Distance { get; set; }
        public string Ride { get; set; }
        public int Temp { get; set; }
        public string Weather { get; set; }
        public string WeatherIcon { get; set; }
        public int Wind { get; set; }
        public string Error { get; set; }
    }
}