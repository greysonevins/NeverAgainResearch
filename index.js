var Twit = require('twit')
var fs = require('fs')

var twit = new Twit({
  consumer_key: process.env.NA_CONSUMER_KEY,
  consumer_secret: process.env.NA_CONSUMER_SECRET,
  access_token: process.env.NA_ACCESS_TOKEN,
  access_token_secret: process.env.NA_ACCESS_TOKEN_SECRET,
  timeout_ms: 60*1000
})

// var stream = twit.stream('statuses/filter', {
//   track: '#neveragain'
// })
//
// stream.on('tweet', function(tweet){
//   console.log(tweet.user.location)
//   console.log(tweet.text+'\n')
// })


function cleanTweets(item, index){
  var newJSON = {}
  if (item.user.location) {
    newJSON = {
      created_at    : item.created_at,
      text          : item.text,
      id            : item.id,
      location      : item.user.location,
      coordinates   : item.coordinates,
      retweet_count : item.retweet_count,
      favorite_count: item.favorite_count
    }
    return newJSON
  }
}

setInterval(function () {
  var recentlyUsed = ""
  fs.readFile("lastused.txt", "utf8", function(err,lastused) {
    recentlyUsed = lastused
  })
  var jsonData = []

  fs.readFile("tweets.txt", function(err,tweets) {
    if (err) throw err;
    jsonData = JSON.parse(tweets)
  })


  twit.get('search/tweets', { q:'#neveragain since:2018-02-18', count: 100, result_type: "recent", max_id: recentlyUsed}, function (err, data, response){
    var cleanedTweets = data.statuses.map(cleanTweets)
    cleanedTweets.map(x => jsonData.push(x))
    jsonData = jsonData.filter(function(n){ return n != undefined})
    var saveJSON = JSON.stringify(jsonData);
    fs.writeFile("tweets.txt", saveJSON , function(err) {
      if(err) {
        return console.log(err);
      }

    });

    var lastusedPt1 = data.statuses.slice(-1).pop().id_str
    if ( parseInt(lastusedPt1.slice(-1)) != 0){
      var replace = parseInt(lastusedPt1.slice(-1)) - 1
      var lastused = lastusedPt1.slice(0, -1) + replace
    } else if (parseInt(lastusedPt1)==0){
      return;
    }else{
      zero = true
      slice = -1
      while (zero) {
        slice -= 1
        if (lastusedPt1.slice(counter) == 0) {
          return;
        } else {
          zero = false
        }

      var replace = parseInt(lastusedPt1.slice(slice)) - 1
      var lastused = lastusedPt1.slice(0, slice) + replace
      }
    }
    console.log(lastused)
    fs.writeFile("lastused.txt", lastused, function(err) {
      if(err) {
        return console.log(err);
      }
    })
    console.log("Done with save")
    console.log("Last Saved", data.statuses.slice(-1).pop().created_at)


    });
}, 20000);
