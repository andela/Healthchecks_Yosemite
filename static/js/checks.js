

//This is a function that was implemented to compute days , hours and minutes from seconds
//The function takes in a single argument which is the total number of seconds
//It returns a four elements array which contains number of days, Hours, minutes and seconds from index 0 to 3 respectively

function getTimes(seconds){
    var times = [0,0,0,0,0,0];
    var tmpTime = parseInt(seconds);

    if (tmpTime >= (3600 * 24 * 365 )){//Total seconds in a year
            var years= parseInt(tmpTime/(3600*24*365));
            tmpTime = tmpTime % (3600 * 24 * 365);
            times[0] = years;
    }

    if (tmpTime >= (3600 * 24 * 31 )){//Total seconds in a month
            var months = parseInt(tmpTime/(3600*24 * 31));
            tmpTime = tmpTime % (3600 * 24 * 31);
            times[1] = months;
    }


    if (tmpTime >= (3600 * 24 )){//Total seconds in a day
            var days = parseInt(tmpTime/(3600*24));
            tmpTime = tmpTime % (3600 * 24);
            times[2] = days;
    }

    if (tmpTime >= 3600){//Total seconds in an hours
            var hours = parseInt(tmpTime/3600);
            tmpTime = tmpTime % 3600;
            times[3] = hours;
    }

    if (tmpTime >= 60){//Total seconds in a minute
            var minutes = parseInt(tmpTime/60);
            tmpTime = tmpTime % 60;
            times[4] = minutes;
    }

    times[5] = tmpTime;
    return times;
}


//This marks the begining of JQuery logic
$(function () {

    $('[data-toggle="tooltip"]').tooltip();

    $(".my-checks-name").click(function() {
        var $this = $(this);

        $("#update-name-form").attr("action", $this.data("url"));
        $("#update-name-input").val($this.data("name"));
        $("#update-tags-input").val($this.data("tags"));
        $('#update-name-modal').modal("show");
        $("#update-name-input").focus();

        return false;
    });

    $('body').on('click','.timeout-grace',function() {
        var $this = $(this);
        var period_times = getTimes($this.data('timeout'));
        var grace_times =  getTimes($this.data('grace'));

        alert(period_times)

        $("#update-timeout-form").attr("action", $this.data("url"));
        $("#years").val(period_times[0]);
        $("#months").val(period_times[1]);
        $("#days").val(period_times[2]);
        $("#hours").val(period_times[3]);
        $("#minutes").val(period_times[4]);
        $("#seconds").val(period_times[5]);

        $("#years1").val(grace_times[0]);
        $("#months1").val(grace_times[1]);        
        $("#days1").val(grace_times[2]);
        $("#hours1").val(grace_times[3]);
        $("#minutes1").val(grace_times[4]);
        $("#seconds1").val(grace_times[5]);


        //periodSlider.noUiSlider.set($this.data("timeout"));
        //graceSlider.noUiSlider.set($this.data("grace"));
        $('#update-timeout-modal').modal({"show":true, "backdrop":"static"});

        return false;
    });

    $(".check-menu-remove").click(function() {
        var $this = $(this);

        $("#remove-check-form").attr("action", $this.data("url"));
        $(".remove-check-name").text($this.data("name"));
        $('#remove-check-modal').modal("show");

        return false;
    });


    $("#my-checks-tags button").click(function() {
        // .active has not been updated yet by bootstrap code,
        // so cannot use it
        $(this).toggleClass('checked');

        // Make a list of currently checked tags:
        var checked = [];
        $("#my-checks-tags button.checked").each(function(index, el) {
            checked.push(el.textContent);
        });

        // No checked tags: show all
        if (checked.length == 0) {
            $("#checks-table tr.checks-row").show();
            $("#checks-list > li").show();
            return;
        }

        function applyFilters(index, element) {
            var tags = $(".my-checks-name", element).data("tags").split(" ");
            for (var i=0, tag; tag=checked[i]; i++) {
                if (tags.indexOf(tag) == -1) {
                    $(element).hide();
                    return;
                }
            }

            $(element).show();
        }

        // Desktop: for each row, see if it needs to be shown or hidden
        $("#checks-table tr.checks-row").each(applyFilters);
        // Mobile: for each list item, see if it needs to be shown or hidden
        $("#checks-list > li").each(applyFilters);

    });

    $(".pause-check").click(function(e) {
        var url = e.target.getAttribute("data-url");
        $("#pause-form").attr("action", url).submit();
        return false;
    });


    $(".usage-examples").click(function(e) {
        var a = e.target;
        var url = a.getAttribute("data-url");
        var email = a.getAttribute("data-email");

        $(".ex", "#show-usage-modal").text(url);
        $(".em", "#show-usage-modal").text(email);

        $("#show-usage-modal").modal("show");
        return false;
    });


    var clipboard = new Clipboard('button.copy-link');
    $("button.copy-link").mouseout(function(e) {
        setTimeout(function() {
            e.target.textContent = "copy";
        }, 300);
    })

    clipboard.on('success', function(e) {
        e.trigger.textContent = "copied!";
        e.clearSelection();
    });

    clipboard.on('error', function(e) {
        var text = e.trigger.getAttribute("data-clipboard-text");
        prompt("Press Ctrl+C to select:", text)
    });


});
