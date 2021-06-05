const Express=require("express");
const Router=Express.Router();


Router.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "*");
    res.header("Access-Control-Allow-Headers", "*");
    next();
});

Router.get("/",(req,res)=>{
    res.send("Resume Module!")
});


Router.post("/upload",(req,res)=>{
    const name = req.body.name;
    res.json({state:true,msg:"Successful!"})
});


module.exports=Router;