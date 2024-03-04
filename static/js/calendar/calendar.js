function processData(dates, date_counts) {
    // 외부에서 실행될 작업을 수행합니다.
    console.log('date : ', dates)
    for (let i=0; i<dates.length; i++) {
        var year = $('.year').text()
        var month_index= $('.month').text()
        var date_itm = $('.this > .date-itm').text()
        var numbers = date_itm.match(/\d+/g);
        var months = 0;
        var day_itm = [];
        if (month_index < 10) {
            months = 0 + month_index;
        }
        for (date of numbers) {
            if (date < 10) {
                day_itm.push(0+date);
            } else{
                day_itm.push(date);
            }
        }
        dates_year = dates[i].split('-')[0]

        if(year == dates_year) {
            month = dates[i].split('-')[1]
            if(months == month) {
                day = dates[i].split('-')[2]
                for (days of day_itm) {
                    if(days == day) {
                        console.log(months , day)
                        if (day < 10) {
                            var day_not_0 = day.replace(/^0+/, '')
                            
                            $('.this > .date-itm').each(function() {
                                var text = $(this).text().trim();
                                if (text == (day_not_0)) {
                                    if (!$(this).parent('.this').hasClass('today')) {
                                        // today 클래스가 없는 경우에만 배경색 변경
                                        $(this).parent('.this').css('background-color', '#A2D2FF');
                                    }
                                }
                            });
                        } else{
                            $('.this > .date-itm').each(function() {
                                var text = $(this).text().trim();
                                if (text == day) {
                                    if (!$(this).parent('.this').hasClass('today')) {
                                        // today 클래스가 없는 경우에만 배경색 변경
                                        $(this).parent('.this').css('background-color', '#A2D2FF');
                                    }
                                }
                            });
                        }

                        
                    }
                }
            }
        }
    }

}



$(document).ready(function(){
    let date = new Date();
    const renderCalender = () => {
        const viewYear = date.getFullYear();
        const viewMonth = date.getMonth();

        document.querySelector('.year').textContent = `${viewYear}`;
        document.querySelector('.month').textContent = `${viewMonth + 1}`;

        const prevLast = new Date(viewYear, viewMonth, 0);
        const thisLast = new Date(viewYear, viewMonth + 1, 0);

        const PLDate = prevLast.getDate();
        const PLDay = prevLast.getDay();

        const TLDate = thisLast.getDate();
        const TLDay = thisLast.getDay();

        const prevDates = [];
        const thisDates = [...Array(TLDate + 1).keys()].slice(1);
        const nextDates = [];

        if (PLDay !== 6) {
            for (let i = 0; i < PLDay + 1; i++) {
                prevDates.unshift(PLDate - i);
            }
        }

        for (let i = 1; i < 7 - TLDay; i++) {
            nextDates.push(i);
        }

        const dates = prevDates.concat(thisDates, nextDates);
        const firstDateIndex = dates.indexOf(1);
        const lastDateIndex = dates.lastIndexOf(TLDate);

        dates.forEach((date, i) => {
            const condition = i >= firstDateIndex && i < lastDateIndex + 1 ?
                'this' :
                'other';
            dates[i] = `
                <div class="date ${condition}">

                    <div class="date-itm">
                        ${date}
                    </div>

                    <div class="date_event">
                        <div class="event-itm"></div>
                    </div>

                </div>
            `;
        });
        
        document.querySelector('.dates').innerHTML = dates.join('');

        const today = new Date();
        if (viewMonth === today.getMonth() && viewYear === today.getFullYear()) {
            for (let date of document.querySelectorAll('.date-itm')) {
                if (+date.innerText === today.getDate()) {
                    date.parentNode.classList.add('today');
                    break;

                }
                
            }
        }
    };

    renderCalender();

    const prevMonth = () => {
        date.setMonth(date.getMonth() - 1);
        renderCalender();
    };

    const nextMonth = () => {
        date.setMonth(date.getMonth() + 1);
        renderCalender();
    };

    const goToday = () => {
        date = new Date();
        renderCalender();
    };
    


    document.querySelector('.go-prev').addEventListener('click', prevMonth);
    document.querySelector('.go-next').addEventListener('click', nextMonth);

})