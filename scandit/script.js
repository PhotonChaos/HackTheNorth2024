 // Import everything
//  import * as SDCCore from "scandit-web-datacapture-core";
//  import * as SDCBarcode from "scandit-web-datacapture-barcode";

// And/or import only needed items (examples)
// import { DataCaptureContext, Camera } from "scandit-web-datacapture-core";
// import { BarcodeCapture } from "scandit-web-datacapture-barcode";

 console.log("Hello!");

 // Functions
 function closeApp() {
    sparkScanView.stopScanning();
 }

 async function startScan() {

    // 
    await configure({
    libraryLocation: new URL("library/engine", document.baseURI).toString(),
    licenseKey: "Amll0jqMH3R+PC4AGzd0RAwAfJjxMrHB4SkxFzM1g9psTix5NUQylWR6N2IBE/5bf0SZ5zAwWGC6dervbDTBmsxHOzuaAPOooHp/f/MXcajoIlhxhyMHnyEfUbutK3TRe2BWNrswAVWNezv50lGEHovK5PWN+CQx9gC5ih/gp6gQC4hgLQdQHkqktHkmY38tTJOYkdSkscz1uBN4qWwmTStQp6XbaJZFxGdti5+EwWhOtfh7uPyM4M5vVZPGA8XcZjAdANCtBM1GbwXFdGHGz8E1GjZQIWPvddr5WHpkUSkPQCEB71MZCKYB/ek/IvT3N6Dv6rRpJ5H/WYfap7TLA2g1QoFoh+JwYgIb50LyVXRrAQc98hVGrahXOjiNnLc/V5lTmcYNXXt7GUX3FIR7RPqtNuQ+Qmde9toja613LCd18GwN1E0zer0lNiV+Ju/y+VbqnjPWDIGHL8HZAwd/evop//976mfNKIpZBtyHvwtSjSFLKleBYXK+aLHJbu7uTMKZNY9JXH+5BBdQgv2q9cRrrxbEtB+75CeiBeu6PdoXBGw+kEa9TVCihL1lpcrHMDcREoIm7X5r84aDQEkhA115HrNQIC9uVOvvWeOwDu1kQGL/i/ZV4uMehW7As7U1uL83LkVvCwPVu0GijP6YTOs5DQ56tRkPmV+eZPfYhtZIlzivx1irxj3ew6Nic9NIYOgxcY9wPNVWadnyhe3f8hRgP0AeExxjcbstJDt3voZWrBtuZd1hGCEryR6Ny5QMBM+75TTV/aDL3QYDzRE5KgiuNMZgTGhLWJxWIheN",
    moduleLoaders: [barcodeCaptureLoader()],
    });

    const dataCaptureContext = await DataCaptureContext.create();

    /////
    const sparkScanSettings = new SparkScanSettings();
    sparkScanSettings.enableSymbologies([Symbology.UPC]);
    const sparkScan = SparkScan.forSettings(settings)

    const viewSettings = new SparkScanViewSettings();
    // setup the desired appearance settings by updating the fields in the object above

    const sparkScanView = SparkScanView.forElement(
    document.body,
    dataCaptureContext,
    sparkScan,
    sparkScanViewSettings,
    );

    const listener = {
    didScan: (sparkScan, session, frameData) => {
        const barcode = session.newlyRecognizedBarcodes[0];
        
    },
    };

    sparkScan.addListener(listener);

    function onBarcodeScanned(sparkScan, session, frameData) {
    // Gather the recognized barcode
    const [barcode] = session.newlyRecognizedBarcodes;
    console.log
    // Do something with the recognized barcode
    
    };
}