(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-7478"],{"0mzU":function(e,t,a){"use strict";var n=a("F8X8");a.n(n).a},17:function(e,t){},18:function(e,t){},19:function(e,t){},"26hR":function(e,t,a){"use strict";a.r(t);var n=a("4d7F"),r=a.n(n),s=a("EUZL"),i=a.n(s),l={props:{beforeUpload:Function,onSuccess:Function},data:function(){return{loading:!1,excelData:{header:null,results:null}}},methods:{generateData:function(e){var t=e.header,a=e.results;this.excelData.header=t,this.excelData.results=a,this.onSuccess&&this.onSuccess(this.excelData)},handleDrop:function(e){if(e.stopPropagation(),e.preventDefault(),!this.loading){var t=e.dataTransfer.files;if(1===t.length){var a=t[0];if(!this.isExcel(a))return this.$message.error("Only supports upload .xlsx, .xls, .csv suffix files"),!1;this.upload(a),e.stopPropagation(),e.preventDefault()}else this.$message.error("Only support uploading one file!")}},handleDragover:function(e){e.stopPropagation(),e.preventDefault(),e.dataTransfer.dropEffect="copy"},handleUpload:function(){this.$refs["excel-upload-input"].click()},handleClick:function(e){var t=e.target.files[0];t&&this.upload(t)},upload:function(e){(this.$refs["excel-upload-input"].value=null,this.beforeUpload)?this.beforeUpload(e)&&this.readerData(e):this.readerData(e)},readerData:function(e){var t=this;return this.loading=!0,new r.a(function(a,n){var r=new FileReader;r.onload=function(e){var n=e.target.result,r=i.a.read(n,{type:"array"}),s=r.SheetNames[0],l=r.Sheets[s],o=t.getHeaderRow(l),u=i.a.utils.sheet_to_json(l);t.generateData({header:o,results:u}),t.loading=!1,a()},r.readAsArrayBuffer(e)})},getHeaderRow:function(e){var t=[],a=i.a.utils.decode_range(e["!ref"]),n=void 0,r=a.s.r;for(n=a.s.c;n<=a.e.c;++n){var s=e[i.a.utils.encode_cell({c:n,r:r})],l="UNKNOWN "+n;s&&s.t&&(l=i.a.utils.format_cell(s)),t.push(l)}return t},isExcel:function(e){return/\.(xlsx|xls|csv)$/.test(e.name)}}},o=(a("UhHk"),a("KHd+")),u=Object(o.a)(l,function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("input",{ref:"excel-upload-input",staticClass:"excel-upload-input",attrs:{type:"file",accept:".xlsx, .xls"},on:{change:e.handleClick}}),e._v(" "),a("div",{staticClass:"drop",on:{drop:e.handleDrop,dragover:e.handleDragover,dragenter:e.handleDragover}},[a("div",{staticClass:"el-upload__text"},[e._v("\n      将文件拖到此处，或\n      "),a("el-button",{staticStyle:{"margin-left":"16px"},attrs:{loading:e.loading,size:"medium",type:"primary"},on:{click:e.handleUpload}},[e._v("点击上传")])],1)])])},[],!1,null,"5566769d",null);u.options.__file="index.vue";var c=u.exports,d=a("NMa0"),p={name:"UploadExcel",components:{UploadExcelComponent:c},data:function(){return{tableData:[{user:"示例",sequence:"1|2|?|3",score:0,type:"默认"}],tableHeader:["user","sequence","score","type"],commit:!1}},methods:{beforeUpload:function(e){return e.size/1024/1024<1||(this.$message({message:"上传文件大小应小于1M.",type:"warning"}),!1)},handleSuccess:function(e){var t=e.results,a=e.header;this.tableData=t,this.tableHeader=a,this.commit=!0},handleUpload:function(){var e=this;Object(d.a)(this.tableData).then(function(){e.$notify({title:"成功",message:"导入成功",type:"success",duration:2e3}),e.tableData=[],e.tableHeader=[],e.commit=!1})},handleReset:function(){this.tableData=[],this.tableHeader=[],this.commit=!1}}},f=(a("0mzU"),Object(o.a)(p,function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"app-container"},[a("upload-excel-component",{attrs:{"on-success":e.handleSuccess,"before-upload":e.beforeUpload}}),e._v(" "),a("div",{directives:[{name:"show",rawName:"v-show",value:e.commit,expression:"commit"}],staticClass:"upload-commit"},[a("el-button",{staticClass:"filter-item",attrs:{type:"primary",size:"medium"},on:{click:e.handleReset}},[e._v("重置")]),e._v(" "),a("el-button",{staticClass:"filter-item",attrs:{type:"primary",size:"medium"},on:{click:e.handleUpload}},[e._v("提交")])],1),e._v(" "),a("el-table",{staticStyle:{width:"100%","margin-top":"20px"},attrs:{data:e.tableData,border:"","highlight-current-row":""}},e._l(e.tableHeader,function(e){return a("el-table-column",{key:e,attrs:{prop:e,label:e}})}))],1)},[],!1,null,"494b125d",null));f.options.__file="uploadExcel.vue";t.default=f.exports},F8X8:function(e,t,a){},HD7a:function(e,t,a){},NMa0:function(e,t,a){"use strict";a.d(t,"a",function(){return r}),a.d(t,"b",function(){return s}),a.d(t,"d",function(){return i}),a.d(t,"c",function(){return l});var n=a("t3Un");function r(e){return Object(n.a)({url:"/api/rules/",method:"post",data:e})}function s(e){return Object(n.a)({url:"/api/rules/"+e+"/",method:"delete"})}function i(e,t){return Object(n.a)({url:"/api/rules/"+e+"/",method:"patch",data:t})}function l(e){return Object(n.a)({url:"/api/rules/",params:e})}},UhHk:function(e,t,a){"use strict";var n=a("HD7a");a.n(n).a}}]);