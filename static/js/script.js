// =====================================================
// URBANTWIN AI - DASHBOARD JAVASCRIPT
// =====================================================


// =====================================================
// CLOCK
// =====================================================

function updateClock() {

    const clock =
        document.getElementById("clock");

    if (!clock) return;

    const now = new Date();

    clock.textContent =
        now.toLocaleTimeString("en-IN", {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        });
}

setInterval(updateClock, 1000);

updateClock();



// =====================================================
// FILE SELECTION
// =====================================================

const trafficFile =
    document.getElementById("trafficFile");

const selectedFile =
    document.getElementById("selectedFile");


if (trafficFile) {

    trafficFile.addEventListener(
        "change",
        function () {

            if (this.files.length > 0) {

                selectedFile.textContent =
                    this.files[0].name;

            } else {

                selectedFile.textContent =
                    "No image selected";
            }

        }
    );
}



// =====================================================
// ANALYZE TRAFFIC
// =====================================================

async function analyzeTraffic() {


    const fileInput =
        document.getElementById("trafficFile");


    // -------------------------------------------------
    // CHECK FILE
    // -------------------------------------------------

    if (
        !fileInput ||
        fileInput.files.length === 0
    ) {

        alert(
            "Please select a traffic image first."
        );

        return;
    }



    // -------------------------------------------------
    // ANALYZE BUTTON
    // -------------------------------------------------

    const analyzeButton =
        document.querySelector(".analyze-btn");


    if (analyzeButton) {

        analyzeButton.disabled = true;

        analyzeButton.textContent =
            "⏳ Analyzing...";
    }



    // -------------------------------------------------
    // FORM DATA
    // -------------------------------------------------

    const formData =
        new FormData();


    formData.append(
        "trafficFile",
        fileInput.files[0]
    );



    try {


        // -------------------------------------------------
        // SEND IMAGE TO FLASK
        // -------------------------------------------------

        const response =
            await fetch(
                "/analyze",
                {
                    method: "POST",
                    body: formData
                }
            );



        // -------------------------------------------------
        // READ JSON RESPONSE
        // -------------------------------------------------

        const result =
            await response.json();


        console.log(
            "UrbanTwin AI Result:",
            result
        );



        // -------------------------------------------------
        // CHECK RESULT
        // -------------------------------------------------

        if (!result.success) {

            alert(
                "Analysis failed:\n" +
                result.message
            );

            return;
        }


        const data =
            result.data;



        // =================================================
        // VEHICLE DETECTION RESULTS
        // =================================================

        const cars =
            document.getElementById("cars");

        if (cars) {

            cars.textContent =
                data.cars;
        }



        const heavy =
            document.getElementById("heavy");

        if (heavy) {

            heavy.textContent =
                data.heavy_vehicles;
        }



        const total =
            document.getElementById("total");

        if (total) {

            total.textContent =
                data.total_vehicles;
        }



        const density =
            document.getElementById("density");

        if (density) {

            density.textContent =
                data.density;
        }



        // =================================================
        // CONGESTION
        // =================================================

        const congestion =
            document.getElementById(
                "congestion"
            );


        if (congestion) {

            congestion.textContent =
                data.congestion.toUpperCase();
        }



        // -------------------------------------------------
        // LEFT PANEL CONGESTION
        // -------------------------------------------------

        const sideCongestion =
            document.getElementById(
                "sideCongestion"
            );


        if (sideCongestion) {

            sideCongestion.textContent =
                data.congestion.toUpperCase();
        }



        // =================================================
        // SIGNAL TIMING
        // =================================================

        const greenTime =
            document.getElementById(
                "greenTime"
            );


        if (greenTime) {

            greenTime.textContent =
                data.green_time;
        }



        const redTime =
            document.getElementById(
                "redTime"
            );


        if (redTime) {

            redTime.textContent =
                data.red_time;
        }



        // =================================================
        // AI RECOMMENDATION
        // =================================================

        const aiRecommendation =
            document.getElementById(
                "aiRecommendation"
            );


        if (aiRecommendation) {

            aiRecommendation.textContent =

                "AI detected " +

                data.total_vehicles +

                " vehicles. " +

                "Traffic density is " +

                data.density +

                " and congestion is " +

                data.congestion +

                ". Recommended signal timing: " +

                data.green_time +

                " seconds GREEN and " +

                data.red_time +

                " seconds RED.";
        }



        // =================================================
        // GAT JUNCTION ANALYSIS
        // =================================================

        if (
            data.junction_analysis &&
            data.junction_analysis.length > 0
        ) {


            data.junction_analysis.forEach(
                function (junction) {


                    const junctionId =
                        String(
                            junction.junction_id
                        );


                    const congestionValue =
                        String(
                            junction.congestion
                        ).toUpperCase();


                    const confidence =
                        junction.confidence;



                    // -------------------------------------
                    // JUNCTION 402
                    // -------------------------------------

                    if (
                        junctionId === "402"
                    ) {

                        const element =
                            document.getElementById(
                                "gat402"
                            );


                        const confidenceElement =
                            document.getElementById(
                                "gat402Confidence"
                            );


                        if (element) {

                            element.textContent =
                                congestionValue;
                        }


                        if (confidenceElement) {

                            confidenceElement.textContent =
                                "Confidence: " +
                                confidence +
                                "%";
                        }

                    }



                    // -------------------------------------
                    // JUNCTION 405
                    // -------------------------------------

                    if (
                        junctionId === "405"
                    ) {

                        const element =
                            document.getElementById(
                                "gat405"
                            );


                        const confidenceElement =
                            document.getElementById(
                                "gat405Confidence"
                            );


                        if (element) {

                            element.textContent =
                                congestionValue;
                        }


                        if (confidenceElement) {

                            confidenceElement.textContent =
                                "Confidence: " +
                                confidence +
                                "%";
                        }

                    }



                    // -------------------------------------
                    // JUNCTION 219
                    // -------------------------------------

                    if (
                        junctionId === "219"
                    ) {

                        const element =
                            document.getElementById(
                                "gat219"
                            );


                        const confidenceElement =
                            document.getElementById(
                                "gat219Confidence"
                            );


                        if (element) {

                            element.textContent =
                                congestionValue;
                        }


                        if (confidenceElement) {

                            confidenceElement.textContent =
                                "Confidence: " +
                                confidence +
                                "%";
                        }

                    }

                }
            );

        }



        // =================================================
        // SYSTEM STATUS
        // =================================================

        const systemStatus =
            document.getElementById(
                "systemStatus"
            );


        if (systemStatus) {

            systemStatus.textContent =
                "YOLO + GAT: Complete";
        }



        // =================================================
        // MODEL INFORMATION
        // =================================================

        console.log(
            "Vision Model: YOLO"
        );


        console.log(
            "Graph Model: GAT"
        );


        console.log(
            "Model Pipeline: YOLO + GAT"
        );


        console.log(
            "Overall Congestion:",
            data.congestion
        );


        console.log(
            "Green Time:",
            data.green_time,
            "seconds"
        );


        console.log(
            "Red Time:",
            data.red_time,
            "seconds"
        );


        console.log(
            "Junction Analysis:",
            data.junction_analysis
        );


        console.log(
            "UrbanTwin AI analysis completed successfully."
        );


    }


    catch (error) {


        console.error(
            "Analysis error:",
            error
        );


        alert(
            "Could not connect to the UrbanTwin AI server.\n\n" +
            "Make sure Flask is running."
        );

    }


    finally {


        if (analyzeButton) {

            analyzeButton.disabled = false;

            analyzeButton.textContent =
                "🤖 Analyze Traffic";
        }

    }

}



// =====================================================
// MAP ZOOM
// =====================================================

function zoomMap(amount) {


    const map =
        document.querySelector(
            ".map-background"
        );


    if (!map) return;


    const current =
        map.dataset.zoom
            ? parseFloat(
                map.dataset.zoom
            )
            : 1;


    let newZoom =
        current + amount;


    if (newZoom < 0.7) {

        newZoom = 0.7;
    }


    if (newZoom > 1.5) {

        newZoom = 1.5;
    }


    map.dataset.zoom =
        newZoom;


    map.style.transform =
        `scale(${newZoom})`;

}