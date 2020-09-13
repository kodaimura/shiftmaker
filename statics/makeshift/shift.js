const weeks = ['日', '月', '火', '水', '木', '金', '土']
const date = new Date()
const y = date.getFullYear()
const m = date.getMonth()

function nextYear (year, month){
	return (month == 11)? ++year : year;
}
function nextMonth (year, month){
	return (month == 11)? 1 : ++month;
}

const startDate = new Date(nextYear(y, m), nextMonth(y, m), 1)
const endDate = new Date(nextYear(nextYear(y, m), nextMonth(y, m)), 
	nextMonth(nextYear(y, m), nextMonth(y, m)), 0)

const countDays = endDate.getDate()
const startDay = startDate.getDay()
let count = 1 
let calendar = ''

calendar += '<h3>' + nextYear(y, m) + '年' + (nextMonth(y, m)+1) + '月' + '</h3>'
calendar += '<table id="cal"><tr>'

let calendar2 = '<table id="cal2"><tr>'

for (day of weeks) {
    calendar += '<th>' + day+ '</th>'
    calendar2 += '<th>' + day+ '</th>'
}
calendar +='</tr>'
calendar2 +='</tr>'
for (let w = 0; w < 6; w++) {
    calendar += '<tr>'
    calendar2 += '<tr>'
    for (let d = 0; d < 7; d++) {
        if (w == 0 && d < startDay) {
            calendar += '<td><input type="text" size="6"></td>'
            calendar2 += '<td></td>'
        } else if (count > countDays) {
            calendar += '<td></td>'
            calendar2 += '<td></td>'
        } else {
            calendar += `<td><font size="3">${count}</font>
                        <input type="text" size="6" id="${count}"></td>`
            calendar2 += `<td id="*${count}"></td>`
            count++
        }
    }
    calendar += '</tr>'
}
calendar += '</table>'
document.getElementById('calendar').innerHTML = calendar
document.getElementById('calendar2').innerHTML = calendar2