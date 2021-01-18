function pollTwitterData() {
  Logger.log(new Date())
  var url = 'https://mobile.twitter.com/timigrossmann';
  var options = {
    'method': 'get',
  };
  var response = UrlFetchApp.fetch(url, options);

  console.log(response)
  
  if (response.getResponseCode() == 200) {
    // if successfull, get the json content of the profile
    var responseBody = response.getContentText();
    // create the regex pattern and get the numbers of tweets, followings, and followers
    var regExp = new RegExp('<div class="statnum">([0-9,]+)<\/div>', "gi");
    var tweets = regExp.exec(responseBody)[1];
    var followings = regExp.exec(responseBody)[1];
    var followers = regExp.exec(responseBody)[1];
    
    Logger.log(tweets, followings, followers);
    
    
    // create a new row in the google spreadsheet
    var spreadSheet = SpreadsheetApp.getActiveSheet();
    var nextRow = 5;
    var nextRowValue = spreadSheet.getRange(nextRow, 1).getValue();
    
    while (nextRowValue != '') {
      nextRow++;
      nextRowValue = spreadSheet.getRange(nextRow, 1).getValue();
    }
    
    // fill in current values
    var currDate = Utilities.formatDate(new Date(), "GMT+1", "yyyy-MM-dd HH:mm");
    spreadSheet.getRange(nextRow, 1).setValue(currDate);
    spreadSheet.getRange(nextRow, 2).setValue(tweets);
    spreadSheet.getRange(nextRow, 3).setValue(followers);
    spreadSheet.getRange(nextRow, 4).setValue(followings);
  }
}

function createTrigger() {
  // Trigger every 6 hours
  ScriptApp.newTrigger('pollTwitterData')
      .timeBased()
      .everyHours(6)
      .create();
}

function deleteTrigger() {
  // Loop over all triggers and delete them
  var allTriggers = ScriptApp.getProjectTriggers();
  
  for (var i = 0; i < allTriggers.length; i++) {
    ScriptApp.deleteTrigger(allTriggers[i]);
  }
}
