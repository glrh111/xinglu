var uploader = Qiniu.uploader({
    runtimes: 'html5,flash,html4',      // 上传模式，依次退化
    browse_button: 'upload_head_button',         // 上传选择的点选按钮，必需
    // 在初始化时，uptoken，uptoken_url，uptoken_func三个参数中必须有一个被设置
    // 切如果提供了多个，其优先级为uptoken > uptoken_url > uptoken_func
    // 其中uptoken是直接提供上传凭证，uptoken_url是提供了获取上传凭证的地址，如果需要定制获取uptoken的过程则可以设置uptoken_func
    // uptoken : '<Your upload token>', // uptoken是上传凭证，由其他程序生成
    // uptoken_url: '/uptoken',         // Ajax请求uptoken的Url，强烈建议设置（服务端提供）
    // uptoken_func: function(file){    // 在需要获取uptoken时，该方法会被调用
    //    // do something
    //    return uptoken;
    // },
    uptoken_url: '/upload-token/head',

    get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的uptoken
    // downtoken_url: '/downtoken',
    // Ajax请求downToken的Url，私有空间时使用，JS-SDK将向该地址POST文件的key和domain，服务端返回的JSON必须包含url字段，url值为该文件的下载地址
    unique_names: false,              // 默认false，key为文件名。若开启该选项，JS-SDK会为每个文件自动生成key（文件名）
    save_key: false,                  // 默认false。若在服务端生成uptoken的上传策略中指定了sava_key，则开启，SDK在前端将不对key进行任何处理
    domain: 'o9hjg7h8u.bkt.clouddn.com',     // bucket域名，下载资源时用到，必需
    container: 'upload_head_container',             // 上传区域DOM ID，默认是browser_button的父元素
    max_file_size: '5mb',             // 最大文件体积限制
    flash_swf_url: '/static/bower_components/plupload/js/Moxie.swf',  //引入flash，相对路径
    max_retries: 3,                     // 上传失败最大重试次数
    dragdrop: true,                     // 开启可拖曳上传
    drop_element: 'upload_head_drop',   // 拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
    chunk_size: '4mb',                  // 分块上传时，每块的体积
    auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传

    //x_vars : {
    //    查看自定义变量
    //    'time' : function(up,file) {
    //        var time = (new Date()).getTime();
              // do something with 'time'
    //        return time;
    //    },
    //    'size' : function(up,file) {
    //        var size = file.size;
              // do something with 'size'
    //        return size;
    //    }
    //},
    init: {
        'FilesAdded': function(up, files) {
            plupload.each(files, function(file) {
                // 文件添加进队列后，处理相关的事情
            });
        },
        'BeforeUpload': function(up, file) {
               // 每个文件上传前，处理相关的事情
        },
        'UploadProgress': function(up, file) {
               // 每个文件上传时，处理相关的事情
               $('#upload_message').html('正在上传...');
        },
        'FileUploaded': function(up, file, info) {
               // 每个文件上传成功后，处理相关的事情
               // 其中info是文件上传成功后，服务端返回的json，形式如：
               // {
               //    "hash": "Fh8xVqod2MQ1mocfI4S4KpRL6D98",
               //    "key": "gogopher.jpg"
               //  }
               // 查看简单反馈
               // ajax source_link to server
               var domain = up.getOption('domain');
               var res = JSON.parse(info);
               var source_link = 'http://' + domain + '/' +res.key; //获取上传成功后的文件的Url
               // generate JSON
               var up_data = {head_url: source_link,};
               var encoded = JSON.stringify(up_data);
               // ajax JSON
               $.ajax({
                  type: 'GET',
                  url: '/save-head-to-db',
                  contentType: 'application/json',
                  data: up_data,
                  // dataType: 'json',
                  success: function(e) {
                    $('#upload_message').html('上传成功！刷新查看');
                  },
                  error: function(e) {
                    $('#upload_message').html('上传失败！状态码：'+e.status_code);
                  },
               });
        },
        'Error': function(up, err, errTip) {
               $('#upload_message').html('');
               $('#upload_message').html(errTip);
        },
        'UploadComplete': function() {
               //队列文件处理完毕后，处理相关的事情
        },
        'Key': function(up, file) {
            // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
            // 该配置必须要在unique_names: false，save_key: false时才生效
            var my_date = new Date();
            var year = my_date.getFullYear();
            var month = my_date.getMonth();
            var date = my_date.getDate();
            var day = my_date.getDay();
            var hour = my_date.getHours();
            var minute = my_date.getMinutes();
            var second = my_date.getSeconds();
            var millisecond = my_date.getMilliseconds();
            // generate cloud file name
            var key = ['head', year, month, date, day, hour, minute, second, millisecond].join('-') + '.jpg';
            // do something with key here
            return key
        }
    },

    filters : {
      max_file_size : '5mb',
      prevent_duplicates: true,
      // Specify what files to browse for
      // mime_types: [
      //     // {title : "flv files", extensions : "flv"} // 限定flv后缀上传格式上传
      //     // {title : "Video files", extensions : "flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,m4v,mp4"}, // 限定flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,m4v,mp4后缀格式上传
      //     {title : "Image files", extensions : "jpg,gif,png"}, // 限定jpg,gif,png后缀上传
      //     // {title : "Zip files", extensions : "zip"} // 限定zip后缀上传
      // ]
    },

});

// // domain为七牛空间对应的域名，选择某个空间后，可通过 空间设置->基本设置->域名设置 查看获取

// // uploader为一个plupload对象，继承了所有plupload的方法



// 文件上传窗口有关
// Refer: http://blog.csdn.net/jbgtwang/article/details/50998075
// with plugin options
// $("#input-id").fileinput({
//   'language': 'zh',
//   'uploadurl': '/upload-head',
//   'allowedFileExtensions': ['jpg', 'gif', 'png'],
//   'showUpload': true,
//   'previewFileType':'any',
//   'browseClass': "btn btn-primary", //按钮样式  
//   'uploadExtraData':{"id": 1, "fileName":'123.mp3'},   
// });

var Q2 = new QiniuJsSDK();
var uploader = Q2.uploader({
    runtimes: 'html5,flash,html4',      // 上传模式，依次退化
    browse_button: 'upload_content_button',         // 上传选择的点选按钮，必需
    // 在初始化时，uptoken，uptoken_url，uptoken_func三个参数中必须有一个被设置
    // 切如果提供了多个，其优先级为uptoken > uptoken_url > uptoken_func
    // 其中uptoken是直接提供上传凭证，uptoken_url是提供了获取上传凭证的地址，如果需要定制获取uptoken的过程则可以设置uptoken_func
    // uptoken : '<Your upload token>', // uptoken是上传凭证，由其他程序生成
    // uptoken_url: '/uptoken',         // Ajax请求uptoken的Url，强烈建议设置（服务端提供）
    // uptoken_func: function(file){    // 在需要获取uptoken时，该方法会被调用
    //    // do something
    //    return uptoken;
    // },
    uptoken_url: '/upload-token/content',

    get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的uptoken
    // downtoken_url: '/downtoken',
    // Ajax请求downToken的Url，私有空间时使用，JS-SDK将向该地址POST文件的key和domain，服务端返回的JSON必须包含url字段，url值为该文件的下载地址
    unique_names: false,              // 默认false，key为文件名。若开启该选项，JS-SDK会为每个文件自动生成key（文件名）
    save_key: false,                  // 默认false。若在服务端生成uptoken的上传策略中指定了sava_key，则开启，SDK在前端将不对key进行任何处理
    domain: 'o9hjg7h8u.bkt.clouddn.com',     // bucket域名，下载资源时用到，必需
    container: 'upload_content_container',             // 上传区域DOM ID，默认是browser_button的父元素
    max_file_size: '5mb',             // 最大文件体积限制
    flash_swf_url: '/static/bower_components/plupload/js/Moxie.swf',  //引入flash，相对路径
    max_retries: 3,                     // 上传失败最大重试次数
    dragdrop: true,                     // 开启可拖曳上传
    // drop_element: 'upload_content_drop',   // 拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
    chunk_size: '4mb',                  // 分块上传时，每块的体积
    auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传

    //x_vars : {
    //    查看自定义变量
    //    'time' : function(up,file) {
    //        var time = (new Date()).getTime();
              // do something with 'time'
    //        return time;
    //    },
    //    'size' : function(up,file) {
    //        var size = file.size;
              // do something with 'size'
    //        return size;
    //    }
    //},
    init: {
        'FilesAdded': function(up, files) {
            plupload.each(files, function(file) {
                // 文件添加进队列后，处理相关的事情
                $('#upload_message').html('');
            });
        },
        'BeforeUpload': function(up, file) {
               // 每个文件上传前，处理相关的事情
        },
        'UploadProgress': function(up, file) {
               // 每个文件上传时，处理相关的事情
               $('#upload_message').html('正在上传...')
        },
        'FileUploaded': function(up, file, info) {
               // 每个文件上传成功后，处理相关的事情
               // 其中info是文件上传成功后，服务端返回的json，形式如：
               // {
               //    "hash": "Fh8xVqod2MQ1mocfI4S4KpRL6D98",
               //    "key": "gogopher.jpg"
               //  }
               // 查看简单反馈
               // ajax source_link to server
               // markdown img: ![图片name](https://url)
               var domain = up.getOption('domain');
               var res = JSON.parse(info);
               var source_link = 'http://' + domain + '/' +res.key; //获取上传成功后的文件的Url
               t1 = document.getElementById("flask-pagedown-body");
               t1.value += '![](' + source_link + '-contentCrop' + ')';
               $('#upload_message').html('上传成功！');
        },
        'Error': function(up, err, errTip) {
               
               //上传出错时，处理相关的事情
               $('#upload_message').html(errTip);
        },
        'UploadComplete': function() {
               //队列文件处理完毕后，处理相关的事情
        },
        'Key': function(up, file) {
            // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
            // 该配置必须要在unique_names: false，save_key: false时才生效
            var my_date = new Date();
            var year = my_date.getFullYear();
            var month = my_date.getMonth();
            var date = my_date.getDate();
            var day = my_date.getDay();
            var hour = my_date.getHours();
            var minute = my_date.getMinutes();
            var second = my_date.getSeconds();
            var millisecond = my_date.getMilliseconds();
            // generate cloud file name
            var key = ['head', year, month, date, day, hour, minute, second, millisecond].join('-') + '.jpg';
            // do something with key here
            return key
        }
    },

    filters : {
      max_file_size : '5mb',
      prevent_duplicates: true,
      // Specify what files to browse for
      // mime_types: [
      //     // {title : "flv files", extensions : "flv"} // 限定flv后缀上传格式上传
      //     // {title : "Video files", extensions : "flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,m4v,mp4"}, // 限定flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,m4v,mp4后缀格式上传
      //     {title : "Image files", extensions : "jpg,gif,png"}, // 限定jpg,gif,png后缀上传
      //     // {title : "Zip files", extensions : "zip"} // 限定zip后缀上传
      // ]
    },

});

moment.locale('zh_CN');