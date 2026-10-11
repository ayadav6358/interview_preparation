(function(){
  function qs(s,el){return (el||document).querySelector(s);}
  function qsa(s,el){return Array.prototype.slice.call((el||document).querySelectorAll(s));}

  // Theme toggle
  try{
    var saved=localStorage.getItem('ai-kb-theme');
    if(saved) document.documentElement.setAttribute('data-theme',saved);
  }catch(e){}
  window.toggleTheme=function(){
    var cur=document.documentElement.getAttribute('data-theme');
    var next = cur==='dark' ? 'light' : (cur==='light' ? 'dark' : (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'light':'dark'));
    document.documentElement.setAttribute('data-theme',next);
    try{localStorage.setItem('ai-kb-theme',next);}catch(e){}
  };

  // Copy buttons on code blocks
  document.addEventListener('DOMContentLoaded',function(){
    qsa('pre').forEach(function(pre){
      var btn=document.createElement('button');
      btn.className='copy-btn';btn.textContent='Copy';
      btn.onclick=function(){
        var code=pre.querySelector('code')?pre.querySelector('code').innerText:pre.innerText;
        navigator.clipboard.writeText(code).then(function(){
          btn.textContent='Copied!';setTimeout(function(){btn.textContent='Copy';},1200);
        }).catch(function(){});
      };
      pre.appendChild(btn);
    });

    // Simple in-page search filter for sidebar
    var search=qs('.searchbox');
    if(search){
      search.addEventListener('input',function(){
        var v=search.value.toLowerCase();
        qsa('.sidebar a').forEach(function(a){
          a.style.display = a.textContent.toLowerCase().indexOf(v)>-1 ? '' : 'none';
        });
      });
    }
  });

  // Progress tracking (dashboard + per-topic checkboxes), via localStorage
  window.markDone=function(id,el){
    try{
      var done=JSON.parse(localStorage.getItem('ai-kb-progress')||'{}');
      done[id]=el.checked;
      localStorage.setItem('ai-kb-progress',JSON.stringify(done));
    }catch(e){}
  };
  window.loadProgress=function(){
    try{
      var done=JSON.parse(localStorage.getItem('ai-kb-progress')||'{}');
      qsa('[data-progress-id]').forEach(function(el){
        if(done[el.getAttribute('data-progress-id')]) el.checked=true;
      });
    }catch(e){}
  };
  document.addEventListener('DOMContentLoaded',window.loadProgress);
})();
