import React, { useEffect, useState } from "react";
import useOLMap from "../hooks/useOlMap";
import { MapContainer as MapComponent } from "../components/MapComponent/OpenLayersComponent";
import LayerSwitcherControl from "../components/MapComponent/OpenLayersComponent/LayerSwitcher/index.js";
import { VectorLayer } from "../components/MapComponent/OpenLayersComponent/Layers";
// import { VectorLayer } from '../MapComponent/OpenLayersComponent/Layers';
import CoreModules from "fmtm/CoreModules";
import { ProjectActions } from "fmtm/ProjectSlice";
// import { CreateProjectActions } from '../../../main/src/store/slices/CreateProjectSlice';
import { CreateProjectActions } from "fmtm/CreateProjectSlice";

function elastic(t) {
  return (
    Math.pow(2, -10 * t) * Math.sin(((t - 0.075) * (2 * Math.PI)) / 0.3) + 1
  );
}
const basicGeojsonTemplate = {
  type: "FeatureCollection",
  features: [],
};
const DefineAreaMap = ({ uploadedGeojson,setGeojsonFile,uploadedDataExtractFile }) => {
  const dispatch = CoreModules.useDispatch();
  const[dataExtractedGeojson, setDataExtractedGeojson] = useState(null);
  const dividedTaskGeojson = CoreModules.useSelector(
    (state) => state.createproject.dividedTaskGeojson
  );

  const { mapRef, map } = useOLMap({
    // center: fromLonLat([85.3, 27.7]),
    center: [0, 0],
    zoom: 1,
    maxZoom: 25,
  });
  
  

  useEffect(() => {
    if(dividedTaskGeojson){

    }else if(uploadedGeojson) {
      const fileReader = new FileReader();
      fileReader.readAsText(uploadedGeojson, "UTF-8");
      fileReader.onload = (e) => {
        //   console.log("e.target.result", e.target.result);
        //   setConvertedJSON(e.target.result);
        dispatch(CreateProjectActions.SetDividedTaskGeojson(e.target.result));
      };
    }else{
      dispatch(CreateProjectActions.SetDividedTaskGeojson(null));
    }
  }, [uploadedGeojson]);
  useEffect(() => {
    if (uploadedDataExtractFile) {
      const fileReader = new FileReader();
      fileReader.readAsText(uploadedDataExtractFile, "UTF-8");
      fileReader.onload = (e) => {
        //   console.log("e.target.result", e.target.result);
        //   setConvertedJSON(e.target.result);
        setDataExtractedGeojson(e.target.result);
        // dispatch(CreateProjectActions.SetDividedTaskGeojson(e.target.result));
      };
    }else{
      // dispatch(CreateProjectActions.SetDividedTaskGeojson(null));
    }
  }, [uploadedDataExtractFile]);
  
  return (
    <div className="map-container" style={{ height: "600px", width: "100%" }}>
      <MapComponent
        ref={mapRef}
        mapInstance={map}
        className="map naxatw-relative naxatw-min-h-full naxatw-w-full"
        style={{
          height: "100%",
          width: "100%",
        }}
      >
        <LayerSwitcherControl />
        {dividedTaskGeojson && (
          <VectorLayer
            geojson={dividedTaskGeojson}
            // stylestyle={{
            //     ...getStyles,
            //     fillOpacity: 100,
            //     lineColor: getStyles.fillColor,
            //     lineThickness: 7,
            //     lineOpacity: 40,
            // }}
            viewProperties={{
              // easing: elastic,
              // animate: true,
              size: map?.getSize(),
              // maxZoom: 15,
              padding: [50, 50, 50, 50],
              // duration: 900,
              constrainResolution: true,
              duration: 2000,
            }}
            onModify={(modifiedGeojson)=>{
              console.log(JSON.parse(modifiedGeojson));
              const parsedJSON = JSON.parse(modifiedGeojson)
              // dispatch(CreateProjectActions.SetDividedTaskGeojson(parsedJSON));
              // Convert GeoJSON to a JSON string
              // var jsonString = JSON.stringify(geoJSONData);

              var f = new File([modifiedGeojson], "AOI.geojson", {type: "application/geo+json" })
              console.log(f,'file F');
              setGeojsonFile(f);


            }}
            zoomToLayer
          />
        )}
        {dataExtractedGeojson && (
          <VectorLayer
            geojson={dataExtractedGeojson}
            // stylestyle={{
            //     ...getStyles,
            //     fillOpacity: 100,
            //     lineColor: getStyles.fillColor,
            //     lineThickness: 7,
            //     lineOpacity: 40,
            // }}
            viewProperties={{
              // easing: elastic,
              // animate: true,
              size: map?.getSize(),
              // maxZoom: 15,
              padding: [50, 50, 50, 50],
              // duration: 900,
              constrainResolution: true,
              duration: 2000,
            }}
            // zoomToLayer
          />
        )}
      </MapComponent>
    </div>
  );
};

DefineAreaMap.propTypes = {};

export default DefineAreaMap;
