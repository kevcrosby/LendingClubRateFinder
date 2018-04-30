d3.select("#submit_button").on("click", function(){
    console.log("Clicked");  
    var annual_income = d3.select("#annual_income").node().value;
    console.log(annual_income);
    
    var investment = d3.select("#investment").node().value;
    console.log(investment);
    
    var dti = d3.select("#dti").node().value;
    console.log(dti);
    
    var delinquency = d3.select("#delinquency").node().value;
    console.log(delinquency);
    
    var purpose = d3.select("#purpose").node().value;
    console.log(purpose);
    
    var home_ownership = d3.select("#home_ownership").node().value;
    console.log(home_ownership);
    
    var employment_length = d3.select("#employment_length").node().value;
    console.log(employment_length);
    
    var term = d3.select("#term").node().value;
    console.log(term);
    
    var grade = d3.select("#grade").node().value;
    console.log(grade);
    
    var state = d3.select("#state").node().value;
    console.log(state);
    
    var data = {
        'annual_income': annual_income,
        'investment': investment,
        'dti': dti,
        'delinquency': delinquency,
        'purpose': purpose,
        'home_ownership': home_ownership,
        'employment_length': employment_length,
        'term': term,
        'grade': grade,
        'state':state 
    }

    console.log(data);
    var url=window.location.origin + "/"
    
    $.post(url, data)
      .then(function(data) {
      console.log(data) 
      d3.select("#rate").text(data)
      drawChart(data)
     });
})