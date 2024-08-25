const handleModel = (() => {
    const imgIn = document.getElementById(`imgIn2`);
    imgIn.addEventListener("change", async () => {
        const formData = new FormData();
        formData.append("file", imgIn.files[0]);

        const res = await fetch(`/wiki`, {
            method: "POST",
            body: formData,
        });

        const data = await res.json();

        if (res.status !== 200) {
            alert(data.message);
            return;
        }

        imgIn.nextElementSibling.textContent = imgIn.files[0].name;
        const imgSrc = document.getElementById(`imgRes2`);

        if (!imgSrc.src.includes(data.filename)) {
            src = imgSrc.src.lastIndexOf("/");
            src = imgSrc.src.substr(0, src + 1);
            imgSrc.src = src + data.filename;
            return;
        }

        src = imgSrc.src.split("?")[0];
        imgSrc.src = src + `?${+new Date().getTime()}`;
    });

    const modelBn = document.getElementById("modelBn2");
    modelBn.addEventListener("click", async () => {
        if (imgIn.files.length === 0) {
            alert("No file part");
            return;
        }

        interfaceHelpers.toggleForm(imgIn, modelBn, false);

        const res = await fetch(`/wiki?order=1`, {
            method: "UPDATE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ filename: imgIn.files[0].name }),
        });

        const data = await res.json();

        if (res.status !== 200) {
            alert(data.message);
            interfaceHelpers.toggleForm(imgIn, modelBn, true);
            return;
        }

        const imgRes = document.getElementById(`imgRes2`);

        if (!imgRes.src.includes(data.filename)) {
            src = imgRes.src.lastIndexOf("/");
            src = imgRes.src.substr(0, src + 1);
            imgRes.src = src + data.filename;

            handleInterface.updateInfo(data.info);
            interfaceHelpers.toggleForm(imgIn, modelBn, true);
            return;
        }

        src = imgRes.src.split("?")[0];
        imgRes.src = src + `?${+new Date().getTime()}`;

        handleInterface.updateInfo(data.info);
        interfaceHelpers.toggleForm(imgIn, modelBn, true);
    });
})();

const handleInterface = (() => {
    interfaceHelpers.setActiveNav("navWiki");
    interfaceHelpers.addTooltipToggle(`header`);

    const paging = 3;
    let currPage = 1;
    let maxPage = 1;

    /* info
     */
    let infoContent = [
        {
            animal: "Animal",
            facts: ["Some very interesting facts..."],
            links: [
                { title: "Links", url: "https://github.com/phongan1x5" },
                { title: "for", url: "https://github.com/kru01" },
                { title: "further reading", url: "https://github.com/TGHuybu" },
            ],
        },
    ];

    const info = document.getElementById(`info`);

    const publishInfo = () => {
        info.innerHTML = "";
        const start = (+currPage - 1) * paging;

        for (let i = start; i < start + paging && i < infoContent.length; i++) {
            const name = document.createElement("h2");
            name.textContent = infoContent[i].animal;

            const facts = document.createElement("p");
            infoContent[i].facts.forEach((fa) => {
                facts.innerHTML += `${fa}<br/>`;
            });

            const links = document.createElement("ul");
            infoContent[i].links.forEach((ln) => {
                const a = `<a href=${ln.url} target='_blank'>🛈  ${ln.title}</a>`;
                links.innerHTML += `<li>${a}</li>`;
            });

            const animal = document.createElement("div");
            animal.append(name, facts, links);
            info.append(animal);
        }
    };

    const updateInfo = (newInfo) => {
        infoContent = newInfo;
        currPage = 1;
        maxPage = Math.ceil(Object.keys(newInfo).length / paging);
        document.querySelector(`#infoNav span`).textContent = ` of ${maxPage}`;
        publishInfo();
    };

    updateInfo(infoContent);

    /* infoNav
     */
    const infoInput = document.querySelector(`#infoNav input`);
    infoInput.addEventListener("change", () => {
        let val = parseInt(infoInput.value);

        if (isNaN(val)) val = currPage;
        else if (val < 1) val = 1;
        else if (val > maxPage) val = maxPage;

        infoInput.setAttribute("value", val);
        infoInput.value = val;
        currPage = val;
        publishInfo(val);
    });

    const clickInfoButton = (inc) => {
        const changeEvent = new Event("change");
        return () => {
            let val = parseInt(infoInput.value);
            if (isNaN(val)) val = currPage;

            infoInput.value = val + inc;
            infoInput.dispatchEvent(changeEvent);
        };
    };

    const infoButtons = document.querySelectorAll(`#infoNav button`);
    infoButtons[0].addEventListener("click", clickInfoButton(-1));
    infoButtons[1].addEventListener("click", clickInfoButton(1));

    return { updateInfo };
})();
