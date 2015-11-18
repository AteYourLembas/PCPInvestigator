<!DOCTYPE html>
<html>
<head>
<title>PCP Details</title>
<link rel="stylesheet" href="/static/css/jq.css" type="text/css" media="print, projection, screen" />
<link rel="stylesheet" href="/static/css/blue.css" type="text/css" id="" media="print, projection, screen" />
<script type="text/javascript" src="/static/js/jquery-latest.js"></script> 
<script type="text/javascript" src="/static/js/jquery.tablesorter.js"></script>
<script type="text/javascript" id="js">

$(document).ready(function() { 
    // call the tablesorter plugin 
    $("#tablesorter-demo").tablesorter({ 
        // sort on the first column and second column, order asc 
        sortList: [[0,0],[1,0]] 
    }); 
}); 
</script>
</head>
<body>
<p>
</br></br>
<div id="main">
<h2>PROVIDER DETAILS</h2>
</br></br>

%	lastname = provider['lastname'] if "lastname" in provider else ""
%	firstname = provider['firstname'] if "firstname" in provider else ""
%	middlename = provider['middlename'] if "middlename" in provider else ""
%	accumulatedscore = 0.0
%	numberofratings = 0.0
%	numberofreviews = 0.0

%	if "ratings" in provider :
% 	   for rating in provider["ratings"] :
%			accumulatedscore += rating['overallscore']
%			numberofratings += 1
%			numberofreviews += rating['numreviews']
%  	   end
% 	end		
</td>


<table cellpadding="3" cellborder="3" width="50%">
<tr>
	<td>NAME</td><td><h3>{{lastname}}, {{firstname}} {{middlename}}</h3></td>
</tr>
<tr>
	<td>SCORE</td><td><b>{{str((accumulatedscore/numberofratings)*100.0)[0:5] if numberofratings > 0 else "" }} %</b></td>
</tr>
<tr>
	<td>PROVIDER ID</td><td>{{provider['providerID']}}</td>
</tr>
<tr>
	<td>ADDRESS</td>
	<td>
		% if "group" in provider :
		{{provider['group']}}<br/>
		% end
		{{provider['type']}}<br/>
		{{provider['address1']}}<br/>
		{{provider['address2']}}<br/>	
		{{provider['address3'] if "address3" in provider else ""}}<br/>			
		{{provider['phone']}}<br/>	
	</td>
</tr>
<tr>
	<td>LAST CHECKED</td><td>{{provider['lastscraped'][0:10] if "lastscraped" in provider else ""}}</td>
</tr>
</table>

<h3>{{ int(numberofreviews) }} REVIEWS</h3>

<div id="demo">
<table cellspacing="1" class="tablesorter" id="tablesorter-demo">
<thead>
<tr>
	<th>Source</th>
	<th>Date</th>
	<th>Score</th>
	<th>Description</th>
	<th>Comments</th>
</tr>
</thead>
<tbody>

%if "ratings" in provider :


%	for rating in provider["ratings"] :
%	overallscore = rating['overallscore'] * 100

		%    for review in rating["reviews"] :
		<tr>
			<td nowrap>
				<a href="{{rating['path']}}">{{rating['sourcetype']}} ({{ rating['numreviews'] }})</a> {{rating['summary'] if rating['summary'] else "" }}
			</td>

			<td nowrap>
				{{review["date"] if "date" in review else ""}}
			</td>
			<td nowrap>
				% if "score" in review and review["score"] != None :
				<b>{{str(review["score"] * 100)[0:25] }} %</b>
				% else :
				Score undefined
				% end
			</td>
			<td nowrap>
				{{review["overalldescription"]}}
			</td>
			<td>
				{{"--".join(review["comments"]) if review["comments"] and review["comments"][0] else "" }}
			</td>


		</tr>
		%     end

%	end
<tbody>
</table>


%end

</div>
</div>
</p>
</body>
</html>