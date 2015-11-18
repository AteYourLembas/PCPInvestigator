<!DOCTYPE html>
<html>
<head>
<title>PCP Report</title>

<link rel="stylesheet" href="/static/css/jq.css" type="text/css" media="print, projection, screen" />
<link rel="stylesheet" href="/static/css/blue.css" type="text/css" id="" media="print, projection, screen" />

<script type="text/javascript" src="/static/js/jquery-latest.js"></script> 
<script type="text/javascript" src="/static/js/jquery.tablesorter.js"></script>
<script type="text/javascript" id="js">

$(document).ready(function() { 
    // call the tablesorter plugin 
    $("table").tablesorter({ 
        // sort on score, then number of reviews, order DESC -- then sort by distance, order ASC
        sortList: [[3,1],[4,1],[6,0]] 
    }); 
}); 
  

</script>

</head>
<body>
<p>

<div id="main">

<h2>PROVIDER SUMMARY</h2>
</br></br>
<div id="demo">

<table cellspacing="1" class="tablesorter">
<thead>
<tr>
	<th>NAME</th>
	<th>SPECIALTY</th>
	<th>SCORE</th>
	<th>REVIEWS</th>
	<th>RATINGS</th>
	<th>ADDRESS</th>
	<th>ESTIMATED DISTANCE</th>	
	<th>RECOMMENDED SEARCHES</th>
	<th>LAST CHECKED</th>
</tr>
</thead>
<tbody>
%for i, provider in enumerate(providers) :
%	lastname = provider['lastname'] if "lastname" in provider else ""
%	firstname = provider['firstname'] if "firstname" in provider else ""
%	middlename = provider['middlename'] if "middlename" in provider else ""
%	title = provider['title'] if "title" in provider else ""
%	accumulatedscore = 0.0
%	numberofratings = 0.0
%	numberofreviews = 0

<tr>

	<td nowrap>
		<a href="/PCPDetails/?providerID={{ provider["providerID"] }}" target="_blank"><b>{{lastname}}, {{firstname}} {{middlename}}</b></a>
	</td>
	<td>
		%if "type" in provider :
		{{provider['type']}}
		% end
	</td>

	<td nowrap>
		%if "ratings" in provider :
		<ul>
		%    for rating in provider["ratings"] :

		%		accumulatedscore += rating['overallscore']
		%		numberofratings += 1
		%		numberofreviews += rating['numreviews']


			<li><a href="{{ rating['path'] }}" target="_blank">{{rating['sourcetype']}} ({{ rating['numreviews'] }}) = {{int(rating['overallscore']*100)}}</a></li>

		%     end
		</ul>
		% end		
	</td>

	<!-- note that we accumulated score is already the average for the source (e.g. vitals.com), so we divide the sum of the scores by the number of sources -->
	<td nowrap>{{str((accumulatedscore/numberofratings)*100.0)[0:5] if numberofratings > 0 else "None" }} %</td>

	<td nowrap>{{numberofreviews}}</td>

	<td>
		{{provider['group'] if 'group' in provider else ""}}<br/>
		{{provider['address1']}}<br/>
		{{provider['address2']}}<br/>	
		{{provider['address3'] if "address3" in provider else ""}}<br/>			
		{{provider['address4'] if "address4" in provider else ""}}<br/>			
		{{provider['phone']}}<br/>	
	</td>
	<td nowrap>{{ distances[i] }}</td>
	<td>
		<ul>
			<li><a href="https://www.google.com/#q={{ lastname }}+{{ firstname }}+{{ title }}+malpractice" target="_blank">Malpractice</a></li>
			<li><a href="https://www.google.com/#q={{ lastname }}+{{ firstname }}+{{ title }}+sanction" target="_blank">Sanctions</a></li>
			<li><a href="https://www.breeze.ca.gov/datamart/searchByName.do" target="_blank">Verify License</a></li>
		</ul>
	</td>
	<td>
		{{provider['lastscraped'][0:10] if "lastscraped" in provider else ""}}	
	</td>

</tr>
%end
</tbody>
</table>
</div>
</div>
</p>
</body>
</html>