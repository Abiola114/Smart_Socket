function doGet(e) { 
Logger.log( JSON.stringify(e) );
var result = 'Ok';
if (e.parameter == 'undefined') {
result = 'No Parameters';
}
else {
var sheet_id = '1iFxryG98OjOKQmDXNAXd43wTngoTV4xjB1RinicTzKk'; // Spreadsheet ID
var sheet = SpreadsheetApp.openById(sheet_id).getActiveSheet();
var newRow = sheet.getLastRow() + 1; 
var rowData = [];
var Curr_Date = new Date();
var Date_ = Utilities.formatDate(Curr_Date, "Africa/Lagos", '   dd/MM/YYYY');
rowData[0] = Date_; // Date in column A
var Curr_Time = Utilities.formatDate(Curr_Date, "Africa/Lagos", 'HH:mm:ss');
rowData[1] = Curr_Time; // Time in column B
for (var param in e.parameter) {
Logger.log('In for loop, param=' + param);
var value = stripQuotes(e.parameter[param]);
Logger.log(param + ':' + e.parameter[param]);
switch (param) {
case 'Voltage':
rowData[2] = value; // Voltage in column C
result = 'Voltage Written on column C'; 
break;
case 'Current':
rowData[3] = value; // Current in column D
result += ' ,Current Written on column D'; 
break; 
case 'pf':
rowData[4] = value; // pf in column E
result += ' ,pf Written on column E'; 
break; 
case 'Power':
rowData[5] = value; //  Power in column F
result += ' ,Power Written on column F'; 
break; 
case 'Energy':
rowData[6] = value; // Energy in column G 
result += ' ,Energy Written on column G'; 
break; 
case 'frequency':
rowData[7] = value; // Energy in column H
result += ' ,frequency Written on column H'; 
break; 
default:
result = "unsupported parameter";
}
}
Logger.log(JSON.stringify(rowData));
var newRange = sheet.getRange(newRow, 1, 1, rowData.length);
newRange.setValues([rowData]);
}
return ContentService.createTextOutput(result);
}
function stripQuotes( value ) {
return value.replace(/^["']|['"]$/g, "");
}

