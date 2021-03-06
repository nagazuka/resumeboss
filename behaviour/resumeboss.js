    function getSummaryStr(text) {
      var str = "";
      if (text) {
        str = text.replace(/\n/g, "<br />");
      }
      return str;
    }

    function getDateStr(dateObj, isCurrent) {
      var str = "";


      if (isCurrent == true || isCurrent == 'true') {
        return 'present';
      }

      if (dateObj) {
        if (dateObj.month) {
          str += dateObj.month;
          str += "-";
        }
        if (dateObj.year) {
          str += dateObj.year;
        }
      }
      return str;
    }

    function scrollTo(elementId) {
      var el = $(elementId).get(0);
      el.scrollIntoView();
    }

    function createSpinner(elementId) {
      var opts = {
        top: 0,
        left: 0
      };
      var target = $(elementId).get(0);
      var spinner = new Spinner(opts).spin(target);
      return spinner;
    }

    function reinitialize() {
      $("#step2-row").addClass("hide");
      $("#step3-row").addClass("hide");
      $("#feedback-row").addClass("hide");

      window.location.reload(false);
    }

    function loadData() {
      $("#step1-status").text("Done!");
      $("#step1-status").addClass("label-success");


      $("#step2-status").text("Loading...");
      $("#step2-status").removeClass("hide");
      $("#step2-row").removeClass("hide");

      var step2Spinner = createSpinner('#step2-spinner');

      IN.API.Profile("me")
      .fields("firstName", "lastName", "headline","summary", "specialties", "skills", "certifications", "educations", "courses", "volunteer","date-of-birth","main-address", "picture-url","public-profile-url", "industry", "positions")
      .result(function(result) {
        $("#step1-logout").removeClass("hide");
        var logoutButton = $("#step1-logout-button")
        logoutButton.on("click", function() {
          IN.User.logout(reinitialize);
          return false;
        });

        var profile = result.values[0];
        var profHTML = "<h2>" + profile.firstName + " " + profile.lastName + "</h2>"; 
        profHTML += "<h4>" + profile.headline + "</h4>"; 

        if ('pictureUrl' in profile) {
          //profHTML += " <button class='close' data-dismiss='alert'>×</button>"
          var pictureUrl = profile.pictureUrl;
          if (pictureUrl) {
            var secureUrl = pictureUrl.replace("http:","https:");
            profHTML += "<p><h6>Photo</h6><img id='pictureUrl' src='" + secureUrl + "' /></p>";
           }
        }

        if ('summary' in profile) {
          //profHTML += " <button class='close' data-dismiss='alert'>×</button>"
          profHTML += "<p><h6>Summary</h6>"+profile.summary+"</p>";
        }

        profHTML += "<h3>Experience</h3>"; 
        var positions = profile.positions.values;
        $.each(positions, function(index, item) {
          //profHTML += " <button class='close' data-dismiss='alert'>×</button>"
          profHTML += "<h4>" + item.company.name + "</h4>"; 
          profHTML += "<h4><small>" + getDateStr(item.startDate) + " - "+ getDateStr(item.endDate, item.isCurrent) + "</small></h4>"; 
          profHTML += "<p>" + getSummaryStr(item.summary) + "</p>"; 
        });

        profHTML += "<h3>Education</h3>"; 
        var educations = profile.educations.values;
        $.each(educations, function(index, item) {
          //profHTML += " <button class='close' data-dismiss='alert'>×</button>"
          profHTML += "<h4>" + item.schoolName + "</h4>"; 
          profHTML += "<h4><small>" + getDateStr(item.startDate) + " - "+ getDateStr(item.endDate) + "</small></h4>"; 
          profHTML += "<p>" + item.fieldOfStudy + ", " + item.degree + "</p>"; 
          profHTML += "<p>" + getSummaryStr(item.notes) + "</p>"; 
        });

        if (certifications in profile && values in profile.certifications) {
          //profHTML += " <button class='close' data-dismiss='alert'>×</button>"
          profHTML += "<h3>Certifications</h3>"; 
          profHTML += "<ul>";
          var certifications = profile.certifications.values;
          $.each(certifications, function(index, item) {
            profHTML += "<li>" + item.name + "</li>"; 
          });
          profHTML += "</ul>";
        }

        //profHTML += " <button class='close' data-dismiss='alert'>×</button>"
        profHTML += "<h3>Skills</h3>"; 
        profHTML += "<p>";
        var skills = profile.skills.values;
        $.each(skills, function(index, item) {
          profHTML += item.skill.name + "   "; 
        });
        profHTML += "</p>";

        step2Spinner.stop();
        $("#step2-status").text("Not yet reviewed");
        $("#profile").html(profHTML);
        $("#additional-info").removeClass("hide");

        //Show confirm buttons after loading
        var confirmButton = $("#step3-generate")
        confirmButton.on("click", function() {
          generateResume(profile);
          _gaq.push(['_trackEvent', 'Generate Resume', 'Button Clicked']);
          return false;
        });
        confirmButton.removeClass("hide");

        var submitButton = $("#feedback-submit");
        submitButton.on("click", function() {
            sendFeedback();
            _gaq.push(['_trackEvent', 'Submit Feedback', 'Button Clicked']);
            return false;
        });
        
        var debugHTML = "<h3>Debug</h3>"; 
        debugHTML += "<code>" + JSON.stringify(result) + "</code>";
        $("#debug").html(debugHTML);
      });

      function sendFeedback() {
        $("#feedback-alert").addClass("hide");
        $("#feedback-success").addClass("hide");
        $("#feedback-submit").button("loading");

        var name = $("#feedback-name-input").val();
        var email_address = $("#feedback-mail-input").val();
        var feedback = $("#feedback-text-input").val();
        var request = $.ajax({
          url: "/resumeboss/feedback",
          type: "POST",
          data: {'email_address': email_address, 'name': name, 'feedback': feedback}
        });

        request.done(function(data) {
          $("#feedback-form").addClass("hide");
          $("#feedback-success").removeClass("hide");
          $("#feedback-status").text("Done!");
          $("#feedback-status").addClass("label-success");
          $("#feedback-submit").button("reset");
          _gaq.push(['_trackEvent', 'Send Feedback', 'Success', data]);
        });

        request.fail(function(jqXHR, textStatus) {
          $("#feedback-alert").removeClass("hide");
          $("#feedback-submit").button("reset");
          var errorMsg = "Request failed: " + textStatus + ", status code " + jqXHR.status; 
          //alert(errorMsg );
          $("#feedback-alert-details").html("Details: " + errorMsg);
          _gaq.push(['_trackEvent', 'Send Feedback', 'Failure', errorMsg]);
        });

      }

      function getAdditionalInfo() {
        var mail = $("#additional-info-mail-input").val();
        var phone = $("#additional-info-phone-input").val();
        var mobile = $("#additional-info-mobile-input").val();
        var additionalInfo = {"mail" : mail, "phone": phone, "mobile": mobile};
        return additionalInfo;
      }

      function generateResume(profile) {
        $("#step2-status").text("Done!");
        $("#step2-status").addClass("label-success");
        $("#step3-row").addClass("hide");
        $("#feedback-row").addClass("hide");
        $("#step3-alert").addClass("hide");
        $("#step3-spinner").empty();

        $("#step3-status").text("Loading...");
        $("#step3-generate").button("loading");
        $("#empty-row-spinner").removeClass("hide");
        var step3Spinner = createSpinner('#step3-spinner');
        scrollTo("#step3-spinner");

        $("#step3-status").removeClass("hide");

        var profStr = JSON.stringify(profile);
        var addStr = JSON.stringify(getAdditionalInfo());
 
        var request = $.ajax({
          url: "/resumeboss/generate",
          type: "POST",
          data: {'template': 'modern-cv', 'profile': profStr, 'additional-info': addStr}
        });

        request.done(function(data) {
          var file = data;
          var linkHTML = "<p><a href='download/" + file + "' target='_blank'><img src='images/pdf1.png'></a></p>"; 
          linkHTML += "<p><a href='download/" + file + "' target='_blank'>Download resume</a></p>"; 
          step3Spinner.stop(); 
          $("#empty-row-spinner").addClass("hide");
          $("#step3-alert").addClass("hide");
          $("#step3-download-link").html(linkHTML);
          $("#step3-download-link").removeClass("hide");
          $("#step3-status").text("Done!");
          $("#step3-generate").button("reset");
          $("#step3-status").addClass("label-success");
          $("#step3-row").removeClass("hide");
          scrollTo("#step3-download-link");
          _gaq.push(['_trackEvent', 'Generate Request', 'Success', file]);
          $("#feedback-row").removeClass("hide");
        });

        request.fail(function(jqXHR, textStatus) {
          step3Spinner.stop();
          $("#step3-alert").removeClass("hide");
          $("#step3-generate").button("reset");
          $("#feedback-row").removeClass("hide");
          var errorMsg = "Request failed: " + textStatus + ", status code " + jqXHR.status; 
          //alert(errorMsg );
          $("#step3-alert-details").html("Details: " + errorMsg);
          _gaq.push(['_trackEvent', 'Generate Request', 'Failure', errorMsg]);
        });

        return false;
      }
    }
