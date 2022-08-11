let renderCalendar = "";
let openModal = "";
let openModalInfo = "";
let modal = "";
let modalInfo = "";
let headlineVisble = true;
let everythingVisble = true;
let date = new Date();
let date_num = "";
let regDate = "";
let configStatus = ""; // False indicating the user has already configured
let daysData = ""; //  save the days data for further proccesing
let selectedDate = "";
document.addEventListener("DOMContentLoaded", () => {
  modalInfo = document.querySelector(".dialog_info");
  openModalInfo = document.querySelector("#info");
  modal = document.querySelector(".dialog");
  openModal = document.querySelector("#settings");
  openModalInfo.addEventListener("click", () => {
    modalInfo.showModal();
  });
  openModal.addEventListener("click", () => {
    modal.showModal();
  });
  if (document.querySelector("#firstUser").textContent == "True")
    openModal.click();
  // set the regDate
  regDate = document.querySelector("#regDate").textContent.split(" ");
  //--
  // set the config status
  configStatus = document.querySelector("#configStatus").textContent;
  //

  //add eventlistner for save config modal
  document.querySelector("#saveConfig").addEventListener("click", () => {
    saveConfig();
  });
  //
  document.querySelector("#topHeadlinesCheck").addEventListener("click", () => {
    if (everythingVisble && headlineVisble === true) {
      document.querySelector("#everythingCol").style.opacity = "25%";
      everythingVisble = false;
    } else {
      document.querySelector("#everythingCol").style.opacity = "100%";
      everythingVisble = true;
    }
  });
  // download d_months months news articles that have been aggregated
  document.querySelector("#d_months").addEventListener("click", () => {
    mStr = "No content";
    fetch(`month_data/${date.getFullYear()} ${date.getMonth() + 1}`)
      .then((response) => response.json())
      .then((response) => {
        if (response["month_articles"].length != 0) mStr = "";
        response["month_articles"].forEach((article) => {
          mStr += JSON.stringify(article) + "\n";
        });
        downloadFile(mStr, `${date.getFullYear()}-${date.getMonth() + 1}.txt`);
      });
  });
  document.querySelector("#d_todays").addEventListener("click", () => {
    heading = document.querySelector("#date_description");
    downloadFile(daysData, `${heading.textContent}.txt`);
  });

  //
  document.querySelector(".days_div").addEventListener("click", (e) => {
    heading = document.querySelector("#date_description");
    if (
      parseInt(e.target.textContent) <= 31 &&
      parseInt(e.target.textContent) >= 1 &&
      e.target.className !== "prev-date" &&
      e.target.className !== "next-date"
    ) {
      date.setDate(e.target.textContent);
      k = date.toDateString().split(" ");
      k[2] = e.target.textContent;
      heading.textContent = k.toString().replaceAll(",", "-");
      editedDate = `${date.getFullYear()}-${
        date.getMonth() + 1
      }-${date.getDate()}`;
      if (date.getMonth() + 1 < 10)
        editedDate = `${date.getFullYear()}-0${
          date.getMonth() + 1
        }-${date.getDate()}`;
      fetch(`day_data/${editedDate}`)
        .then((response) => response.json())
        .then((response) => {
          newsTab = document.querySelector("#news_content");
          newsTab.innerHTML = "";
          daysData = "";
          // save the days data so we dont have to fetch again for downloading
          if (response["days_articles"].length === 0) {
            newsTab.innerHTML = `<div class="text-center mt-5 fw-bold fs-3">No content</div>`;
            daysData += "No content";
          }
          response["days_articles"].forEach((article) => {
            daysData += `${JSON.stringify(article) + "\n"}`;
            newsTab.innerHTML += `<div class="col-12">
          <div class="card bg-dark ">
            <div class="row">
              <div class="col-12">
                <img src=${article["article_image_url"]} class="card-img" alt=${article["title"]} style="background-size:cover;">
              </div>
            </div>
            <div class="row">
              <div class="col-12 p-2">
                <div class="card-body">
                  <a href=${article["article_url"]} target='_blank'><h5 class="card-title fw-bolder text-start" data-news="title">${article["title"]}</h5></a>
                  <p class="card-text text-start mt-3">${article["discription"]}</p>
                  <hr />
                  <p class="card-text text-start mt-3">${article["content"]}</p>
                  <p class="card-text text-center fw-bold fs-2"><small >${article["author"]}</small></p>
                </div>
              </div>
           </div>
          </div>
         </div>`;
          });
        });
    }
  });
  //

  document.querySelector("#everythingCheck").addEventListener("click", () => {
    if (headlineVisble && everythingVisble === true) {
      document.querySelector("#headlineCol").style.opacity = "15%";
      headlineVisble = false;
    } else {
      document.querySelector("#headlineCol").style.opacity = "100%";
      headlineVisble = true;
    }
  });

  document.getElementById("infoTab").addEventListener("animationend", () => {
    document.getElementById("infoTab").style.animation = "none";
    document.getElementById("infoTab").innerHTML = "";
    setTimeout(() => {
      document.getElementById("infoTab").style.animation = "";
    }, 0.5);
  });

  // setting Up the calander
  date_num = date.getDate();
  renderCalendar = () => {
    date.setDate(1);
    const monthDays = document.querySelector(".days_div");

    const lastDay = new Date(
      date.getFullYear(),
      date.getMonth() + 1,
      0
    ).getDate();

    const prevLastDay = new Date(
      date.getFullYear(),
      date.getMonth(),
      0
    ).getDate();

    const firstDayIndex = date.getDay();

    let nextDays = 1;

    const months = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];
    date.setDate(date_num);
    document.querySelector(".date h1").innerHTML = months[date.getMonth()];
    document.querySelector(".date h1").innerHTML += " " + date.getFullYear();
    document.querySelector(".date p").innerHTML = "Today: ";
    document.querySelector(".date p").innerHTML += new Date().toDateString();

    let days = "";
    let days_row = `<div class="days_row">`;
    let counter = 1;
    for (let x = firstDayIndex; x > 0; x--) {
      days_row += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
      if (counter === 7) {
        days_row += "</div>";
        days += days_row;
        days_row = `<div class="days_row">`;
        counter = 0;
      }
      counter++;
      nextDays++;
    }
    if (counter === 1) days_row = `<div class="days_row">`;
    counter--;
    for (let i = 1; i <= lastDay; i++) {
      if (
        months[date.getMonth()] === processRegDate()[0] &&
        date.getFullYear() == processRegDate()[2] &&
        i == processRegDate()[1]
      ) {
        days_row += `<div class="reg_date">${i}</div>`;
        counter++;
        nextDays++;
      } else if (
        i === new Date().getDate() &&
        date.getMonth() === new Date().getMonth() &&
        date.getFullYear() == new Date().getFullYear()
      ) {
        days_row += `<div class="today">${i}</div>`;
        counter++;
        nextDays++;
      } else {
        days_row += `<div class=monthsDays>${i}</div>`;
        counter++;
        nextDays++;
      }
      if (counter === 7) {
        days_row += "</div>";
        days += days_row;
        days_row = `<div class="days_row">`;
        counter = 0;
      }
    }
    if (counter === 0) days_row = `<div class="days_row">`;
    let i = 1;
    counter++;
    for (let j = nextDays; j <= 42; j++) {
      days_row += `<div class="next-date">${i}</div>`;
      if (counter === 7) {
        days_row += "</div>";
        days += days_row;
        days_row = `<div class="days_row">`;
        counter = 0;
      }
      counter++;
      i++;
    }
    if (counter !== 1) {
      days_row += "</div>";
      days += days_row;
    }
    monthDays.innerHTML = days;
  };

  document.querySelector("#prev").addEventListener("click", () => {
    date.setFullYear(
      date.getMonth() === 0 ? date.getFullYear() - 1 : date.getFullYear()
    );
    date.setMonth(date.getMonth() === 0 ? 11 : date.getMonth() - 1);
    fetchMonthData();
  });

  document.querySelector("#next").addEventListener("click", () => {
    date.setFullYear(
      date.getMonth() === 11 ? date.getFullYear() + 1 : date.getFullYear()
    );
    date.setMonth(date.getMonth() === 11 ? 0 : date.getMonth() + 1);
    fetchMonthData();
  });

  fetchMonthData();
  intervalId = setInterval(updateStatus, 1200000); // 20min interval
});
function updateConfigInfo(type, context) {
  configBar = document.querySelector("#configDisplay");
  configBar.innerHTML = "";
  if (type === "Everything")
    configBar.innerHTML = `<div class="row mb-1">
     <div class="col-3">Type</div>
     <div class="col-9">Everything</div>
   </div> 
   <div class="row mb-1">
     <div class="col-3">queryString</div>
     <div class="col-9">${context["queryString"]}</div>
   </div> 
   <div class="row mb-1">
     <div class="col-3">searchIn</div>
     <div class="col-9">${context["searchIn"]}</div>
   </div> 
   <div class="row mb-1">
     <div class="col-3">sources</div>
     <div class="col-9">${context["sources_everything"]}</div>
   </div> 
   <div class="row mb-1">
     <div class="col-3">language</div>
     <div class="col-9">${context["language"]}</div>
   </div>`;
  else
    configBar.innerHTML = `<div class="row mb-1">
   <div class="col-3">Type</div>
   <div class="col-9">TopHeadlines</div>
 </div> 
 <div class="row mb-1">
   <div class="col-3">queryString</div>
   <div class="col-9">${context["queryString"]}</div>
 </div> 
 <div class="row mb-1">
   <div class="col-3">sources</div>
   <div class="col-9">${context["sources_headlines"]}</div>
 </div> 
 <div class="row mb-1">
   <div class="col-3">catagory</div>
   <div class="col-9">${context["catagory"]}</div>
 </div> 
 <div class="row mb-1">
   <div class="col-3">country</div>
   <div class="col-9">${context["country"]}</div>
 </div>`;
}
function downloadFile(data, name = "Json.txt") {
  const blob = new Blob([data], { type: "octet-stream" });
  const href = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement("a"), {
    href,
    style: "display:none",
    download: name,
  });
  document.body.appendChild(a);
  a.click();
  URL.revokeObjectURL(href);
  a.remove();
}

function fetchMonthData() {
  renderCalendar();

  fetch(`month_info/${date.getFullYear()} ${date.getMonth() + 1}`)
    .then((response) => response.json())
    .then((responseJson) => {
      daysWithContent = responseJson["days_filled_content"];
      document.querySelectorAll(".monthsDays").forEach((day) => {
        if (daysWithContent.indexOf(parseInt(day.textContent)) != -1)
          // markdates with article content
          day.className = "hasContent";
      });
    });
}
async function updateStatus() {
  try {
    fetchMonthData();
    const response = await fetch("/aggregate_info");
    const responseJson = await response.json();
    if (responseJson["config_error"])
      runInfoTab(
        "Config error detected check i icon for more information",
        "text-center fs-3 fw-bold alert alert-danger"
      );
    else {
      runInfoTab(
        `Todays article count ${responseJson["todays_article_count"]}`,
        "text-center fs-3 fw-bold alert alert-success"
      );
    }
    document.querySelector("#notificationBar").textContent =
      responseJson["info"];
  } catch (err) {
    console.log(err);
    clearInterval(intervalId);
  }
}
function runInfoTab(message, type) {
  infoTab = document.getElementById("infoTab");
  infoTab.className = type;
  infoTab.innerHTML = "";
  infoTab.innerHTML = message;
  infoTab.style.animationPlayState = "running";
}
function processRegDate() {
  reg = [];
  regDate.forEach((e) => {
    reg.push(e.replace(",", ""));
  });
  return reg;
}
function saveConfig() {
  if (headlineVisble === true && everythingVisble) {
    runInfoTab(
      "Config Error :select one of the checkBoxes",
      "text-center fs-3 fw-bold alert alert-danger"
    );
    return false;
  }
  let configStatment =
    configStatus === "True" ? "Config Updated" : "Config Created";
  const selected_every = document.querySelectorAll(
    "#sources_everything option:checked"
  );
  const selected_head = document.querySelectorAll(
    "#sources_headlines option:checked"
  );
  const selected_search_option = document.querySelectorAll(
    "#searchIn option:checked"
  );
  const values_search_option = Array.from(selected_search_option).map(
    (el) => el.value
  );
  const values_everything = Array.from(selected_every).map((el) => el.value);
  const values_head = Array.from(selected_head).map((el) => el.value);
  console.log(values_everything);
  queryString = document.querySelector("#queryString").value;
  searchIn = values_search_option;
  sources_everything = values_everything;
  language = document.querySelector("#language").value;
  everythingCheck = document.querySelector("#everythingCheck").checked;
  catagory = document.querySelector("#category").value;
  country = document.querySelector("#country").value;
  sources_headlines = values_head;
  topHeadlinesCheck = document.querySelector("#topHeadlinesCheck").checked;

  if (everythingCheck)
    fetch("/config_save", {
      method: "POST",
      body: JSON.stringify({
        check: "Everthing",
        queryString: queryString,
        searchIn: searchIn,
        sources_everything: sources_everything,
        language: language,
      }),
    })
      .then((response) => {
        if (response.status == 200) {
          runInfoTab(
            `${configStatment} : Aggregation start may take an hour   `,
            "text-center fs-3 fw-bold alert alert-success"
          );
          configStatus = false;
          document.querySelector(
            "#notificationBar"
          ).textContent = `Config saved.
  Message : your request is qeued for daily content.Be sure to check this tab regularly
  any config or result related issues are posted here`;
          updateConfigInfo("Everything", {
            queryString: queryString,
            searchIn: searchIn,
            language: language,
            sources_everything: sources_everything,
          });
        }
      })
      .catch(() =>
        runInfoTab(
          `${configStatment} : `,
          "text-center fs-3 fw-bold alert alert-danger"
        )
      );
  else if (topHeadlinesCheck)
    fetch("/config_save", {
      method: "POST",
      body: JSON.stringify({
        check: "Headlines",
        queryString: queryString,
        catagory: catagory,
        country: country,
        sources_headlines: sources_headlines,
      }),
    })
      .then((response) => {
        if (response.status == 200) {
          runInfoTab(
            `${configStatment} : Aggregation start may take an hour  `,
            "text-center fs-3 fw-bold alert alert-success"
          );
          configStatus = false;
          document.querySelector(
            "#notificationBar"
          ).textContent = `Config saved.
  Message : your request is qeued for daily content.Be sure to check this tab regularly
  any config or result related issues are posted here`;
          updateConfigInfo("TopHeadlines", {
            queryString: queryString,
            catagory: catagory,
            country: country,
            sources_headlines: sources_headlines,
          });
        }
      })
      .catch(() =>
        runInfoTab(
          `${configStatment} : `,
          "text-center fs-3 fw-bold alert alert-danger"
        )
      );
}
