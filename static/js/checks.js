

//This is a function that was implemented to compute days , hours and minutes from seconds
//The function takes in a single argument which is the total number of seconds
//It returns a four elements array which contains number of days, Hours, minutes and seconds from index 0 to 3 respectively

function getTimes(seconds){
    var times = [0,0,0,0];
    var tmpTime = parseInt(seconds);

    if (tmpTime >= (3600 * 24 )){//Total seconds in a day
            var days = parseInt(tmpTime/(3600*24));
            tmpTime = tmpTime % (3600 * 24);
            times[0] = days;
    }

    if (tmpTime >= 3600){//Total seconds in an hours
            var hours = parseInt(tmpTime/3600);
            tmpTime = tmpTime % 3600;
            times[1] = hours;
    }

    if (tmpTime >= 60){//Total seconds in a minute
            var minutes = parseInt(tmpTime/60);
            tmpTime = tmpTime % 60;
            times[2] = minutes;
    }

    times[3] = tmpTime;
    return times;
}


//This marks the begining of JQuery logic
$(function () {
    var MINUTE = {name: "minute", nsecs: 60};
    var HOUR = {name: "hour", nsecs: MINUTE.nsecs * 60};
    var DAY = {name: "day", nsecs: HOUR.nsecs * 24};
    var WEEK = {name: "week", nsecs: DAY.nsecs * 7};
    var UNITS = [WEEK, DAY, HOUR, MINUTE];

    var secsToText = function(total) {
        var remainingSeconds = Math.floor(total);
        var result = "";
        for (var i=0, unit; unit=UNITS[i]; i++) {
            if (unit === WEEK && remainingSeconds % unit.nsecs != 0) {
                // Say "8 days" instead of "1 week 1 day"
                continue
            }

            var count = Math.floor(remainingSeconds / unit.nsecs);
            remainingSeconds = remainingSeconds % unit.nsecs;

            if (count == 1) {
                result += "1 " + unit.name + " ";
            }

            if (count > 1) {
                result += count + " " + unit.name + "s ";
            }
        }

        return result;
    }

    var periodSlider = document.getElementById("period-slider");
    noUiSlider.create(periodSlider, {
        start: [20],
        connect: "lower",
        range: {
            'min': [60, 60],
            '33%': [3600, 3600],
            '66%': [86400, 86400],
            '83%': [604800, 604800],
            'max': 2592000,
        },
        pips: {
            mode: 'values',
            values: [60, 1800, 3600, 43200, 86400, 604800, 2592000],
            density: 4,
            format: {
                to: secsToText,
                from: function() {}
            }
        }
    });

    periodSlider.noUiSlider.on("update", function(a, b, value) {
        var rounded = Math.round(value);
        $("#period-slider-value").text(secsToText(rounded));
        $("#update-timeout-timeout").val(rounded);
    });


    var graceSlider = document.getElementById("grace-slider");
    noUiSlider.create(graceSlider, {
        start: [20],
        connect: "lower",
        range: {
            'min': [60, 60],
            '33%': [3600, 3600],
            '66%': [86400, 86400],
            '83%': [604800, 604800],
            'max': 2592000,
        },
        pips: {
            mode: 'values',
            values: [60, 1800, 3600, 43200, 86400, 604800, 2592000],
            density: 4,
            format: {
                to: secsToText,
                from: function() {}
            }
        }
    });

    graceSlider.noUiSlider.on("update", function(a, b, value) {
        var rounded = Math.round(value);
        $("#grace-slider-value").text(secsToText(rounded));
        $("#update-timeout-grace").val(rounded);
    });


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
        period_times = getTimes($this.data('timeout'));
        grace_times =  getTimes($this.data('grace'));

        $("#update-timeout-form").attr("action", $this.data("url"));
        $("#update-timeout-form #days").val(period_times[0]);
        $("#update-timeout-form #hours").val(period_times[1]);
        $("#update-timeout-form #minutes").val(period_times[2]);
        $("#update-timeout-form #seconds").val(period_times[3]);

        $("#update-timeout-form").attr("action", $this.data("url"));
        $("#update-timeout-form #days1").val(grace_times[0]);
        $("#update-timeout-form #hours1").val(grace_times[1]);
        $("#update-timeout-form #minutes1").val(grace_times[2]);
        $("#update-timeout-form #seconds1").val(grace_times[3]);


        periodSlider.noUiSlider.set($this.data("timeout"));
        graceSlider.noUiSlider.set($this.data("grace"));
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
