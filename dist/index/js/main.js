new Vue({
    el:"#app",
    data:{
        prizeList:[],
        prizeSearchList:[],
        username:'',
        loginname:'',
        searchname:'',
        loginMoCotent:'',
        lottyNum:0,
        curpage:1,
        totalpage:0,
        layerBg:false,
        loginFlag:false,
        prizerusultFlag:false,
        prizeModalFlag:false,
        pagenav:false
    },
    filters:{
        formattime:function(value){
            return value.slice(0,10) +' '+ value.slice(11,19)
        }
    },
    mounted:function(){
        // this.$nextTick(function(){
            this.prizelist();

        // })
    },
    methods:{
        prizelist:function(){
            var _this=this;
            this.$http.get("/api/records/").then(function(data){
                _this.prizeList = data.data;
            })
        },
        login:function () {
            var _this=this;
            if(this.loginname==''){
                alert('请输入会员账号')
            }else{
                this.$http.post("/api/records/",{'user': this.loginname,'action': 'login'}).then(function(data){
                    this.loginFlag=false
                    this.layerBg=false
                    if(data.data.code==2){
                        _this.loginMoCotent = data.data.error;
                        this.prizeModalFlag=true
                        this.layerBg=true
                    }else if(data.data.code==3){
                        _this.loginMoCotent = data.data.error;
                        this.prizeModalFlag=true
                        this.layerBg=true
                    }else{
                        _this.username = data.data.user;
                        _this.lottyNum = data.data.score;
                    }

                })
            }
        },
        search:function (n) {
            var _this=this;
            if(this.searchname==''){
                alert('请输入会员账号')
            }else {
                if(n==1){this.curpage=1}
                this.$http.get("/api/records/",{params:{user:this.searchname,page_size:5,page:this.curpage}}).then(function(data){
                    console.log(data);
                    _this.prizeSearchList = data.data.results;
                    _this.totalpage = ((data.data.count%5!==0)?(Math.floor(data.data.count/5)+1):(data.data.count/5));
                    if(data.data.count>0){
                        _this.pagenav=true
                    }
                })
            }
        },

        changepage:function(num){
            if(num<1&&this.curpage>1){
                this.curpage--
                this.search()
            }else if(num>1&&this.curpage<this.totalpage){
                console.log(this.curpage)
                console.log(this.totalpage)
                this.curpage++
                this.search()
            }
        },
        zadan:function (m) {
            if(this.username==''){
                this.loginFlag=true
                this.layerBg=true
            }else{
                if(this.lottyNum==0){
                    alert("抽奖次数不足！")
                }else{
                    var _this=this;
                    this.prizeModalFlag=true
                    this.layerBg=true
                    this.$http.post("/api/records/",{'user':this.username}).then(function(data){
                        this.lottyNum--
                        _this.loginMoCotent = data.data.prizeName;
                        $('#myEgg'+m).attr('src','images/egg-hover.png')
                    })
                }
            }
        }
    }
})


