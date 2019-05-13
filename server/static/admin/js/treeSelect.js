function treeMenu(a){
   this.tree=a||[];
   this.groups={};
   this.num = 0;
};
treeMenu.prototype={
    init:function(pid){
        this.group();
        return this.getDom(this.groups[pid]);
    },
    group:function(){
        for(var i=0;i<this.tree.length;i++){
            if(this.groups[this.tree[i].pid]){
                this.groups[this.tree[i].pid].push(this.tree[i]);
            }else{
                this.groups[this.tree[i].pid]=[];
                this.groups[this.tree[i].pid].push(this.tree[i]);
            }
        }
        return this.groups;
    },
      getDom: function(a) {
        this.num++
        if (!a) {
          return '';
        } //当前节点不存在的时候，退出
          var html = '<ul class="dropdown-menu">';
          if(this.num==1){
            html = '<ul class="dropdown-menu multi-level">';
          }

        for (var i = 0; i < a.length; i++) {

              if(this.groups[a[i].id]){
                  html += '<li class="dropdown-submenu" data-cid="'+a[i].id+'"><a href="javascript:void(0);">' + a[i].name+'</a>';
              }else{
                  html += '<li data-cid="'+a[i].id+'"><a href="javascript:void(0);">' + a[i].name+'</a>';
              }

          html += this.getDom(this.groups[a[i].id]);
          html += '</li>';
        };
        html += '</ul>';
        return html;
      }
};
// var html=new treeMenu(data).init(0);




