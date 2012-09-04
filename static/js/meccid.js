function addTask(someday)
    {

        newTaskText = $('#newTask').val();
        taskNumber = $('#numberOfTasks').val();

        if(newTaskText.length > 100)
        {
            $('.errorMessage').show();
        }
        else if ( newTaskText.length > 0 && taskNumber>0)
        {
            $('.errorMessage').hide();

            taskNumber = $('#numberOfTasks').val();
            taskNumber--;
            $('#numberOfTasks').val(taskNumber);
            $('#labelNumberOfTasks').html(taskNumber);

            url = "/manage_task/";
            var returnedID;
            data =  {
                'task_text': newTaskText,
                'givendate': someday,
                'option' : 1
            };
            jQuery.ajax(
                {
                    'type': 'GET',
                    'url': url,
                    'data': data,
                    'fail': function(){
                        alert('failure here!');
                    },
                    'success': function(data)
                    {
                        returnedID = data;
                        con = $('#tasks').html();
                        con += "<tr  class='taskItem' id='taskID_";
                        con += returnedID;
                        con += "'><td class'taskColumn'><img id='imageID_";
                        con += returnedID;
                        con += "' src='/static/images/task-icon-1.jpg'  width='16' height='16'><span id='textID_";
                        con += returnedID;
                        con += "' class='taskText taskText_1'>";
                        con += newTaskText;
                        con += " </span><td class='updateMenu'><img src='/static/images/cross.png' width='16' height='16' onclick = 'markTask(";
                        con += returnedID;
                        con += ",3)'>";
                        con += "<img src='/static/images/tick.png' width='16' height='16' onclick = 'markTask(";
                        con += returnedID;
                        con += ",2)'>";

                        con += "<img src='/static/images/minus.png' width='16' height='16' onclick = 'deleteTask(";
                        con += returnedID;
                        con += ")'> </td></tr>";
                        $('#tasks').html(con);
                    }
                });
        }
        $('#newTask').val('');
    }
    function deleteTask(id)
    {
        url = "/manage_task/";
        var returnedID;
        data =  {
            'id': id,
            'option' : 2
        };
        jQuery.ajax(
            {
                'type': 'GET',
                'url': url,
                'data': data,
                'fail': function(){
                    alert('failure here!');
                },
                'success': function(data)
                {
                    returnedID = data;
                    $('#taskID_'+id).remove();
                    taskNumber = $('#numberOfTasks').val();
                    taskNumber++;
                    $('#numberOfTasks').val(taskNumber);
                    $('#labelNumberOfTasks').html(taskNumber);
                }
            });




    }
    function saveButton()
    {
        $('#taskForm').submit();
    }

    function markTask(id,classN)
    {
        url = "/manage_task/";

        data =  {
            'task_id':id,
            'task_class':classN,
            'option': 3
        };
        jQuery.ajax(
            {
                'type': 'GET',
                'url': url,
                'data': data,
                'fail': function(){
                    alert('failure here!');
                },
                'success': function(data)
                {
                    source = "/static/images/task-icon-";
                    source += classN;
                    source += ".jpg";

                    $('#imageID_'+id).attr("src", source);

                    $('#textID_'+id).removeClass();
                    $('#textID_'+id).addClass("taskText_"+classN);

                }
            });
    }
    function showMenu(id)
    {
        $('updateMenu_'+id).style('display = block');
    }
    function submitSearch()
    {
        keyword = $('#id_searchBox').val();
        if( keyword.length > 0)
        {
            $('#id_searchForm').submit();
        }
    }