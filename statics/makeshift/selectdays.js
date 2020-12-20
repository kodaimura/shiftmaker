const weeks = ['日', '月', '火', '水', '木', '金', '土']
const date = new Date()
const y = date.getFullYear()
const m = date.getMonth()

function nextYear (year, month){
	return (month == 11)? ++year : year;
}
function nextMonth (year, month){
	return (month == 11)? 0 : ++month;
}

const startDate = new Date(nextYear(y, m), nextMonth(y, m), 1)
const endDate = new Date(nextYear(nextYear(y, m), nextMonth(y, m)), 
	nextMonth(nextYear(y, m), nextMonth(y, m)), 0)

const countDays = endDate.getDate()
const startDay = startDate.getDay()
let count = 1 
let calendar = ''

calendar += '<h4>' + nextYear(y, m) + '/' + (nextMonth(y, m)+1) + '</h4>'
calendar += '<table>'

for (day of weeks) {
    calendar += '<td>' + day+ '</td>'
}

for (let w = 0; w < 6; w++) {
    calendar += '<tr>'

    for (let d = 0; d < 7; d++) {
        if (w == 0 && d < startDay) {
            calendar += '<td></td>'
        } else if (count > countDays) {
            calendar += '<td></td>'
        } else {
            calendar += `<td class="not_selected" id="${count}">` + count+ '</td>'
            count++
        }
    }
    calendar += '</tr>'
}
calendar += '</table>'

document.getElementById('calendar').innerHTML = calendar


document.addEventListener('DOMContentLoaded', function(event){
    let days = []
    for (let i = 1; i <= countDays; i++) {
        document.getElementById(`${i}`).addEventListener('click', 
            function(event){
                if (this.className == 'not_selected'){
                    this.className = 'selected'
                    days.push(Number(this.innerHTML))
                    document.getElementById('rest_days').value = JSON.stringify(days.sort((a,b) => a-b))
                }else{
                    this.className = 'not_selected'
                    days = days.filter(d => d !== Number(this.innerHTML))
                    document.getElementById('rest_days').value = JSON.stringify(days.sort((a,b) => a-b))
                }
            })
    }
}) 
