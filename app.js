const Express=require("express");
const BodyParser=require("body-parser");
const Resume=require("./routes/resume");
const cors=require("cors");

const App=Express();
const port=3000;

App.use(BodyParser.json());
App.use("/resume",Resume);
App.use(cors());

App.listen(port,()=>{
    console.log("Port Works!");
});


App.get("/",(req,res)=>{
    res.send("Candidate Recommender!")
});