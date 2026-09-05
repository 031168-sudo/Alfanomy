from pathlib import Path

p = Path('project/app/src/main/assets/code.js')
s = p.read_text(encoding='utf-8')

# Use exactly the same authenticated update operation that is started by exp.login:
# login success -> onNewData(e) -> getUpdateAsync().  Status only exposes a small
# wrapper around that existing operation; it does not create another server API.
old_api = '''exp.requestSignalRefresh=function(e){var t={};t[e]=0;return server.async({name:"update",data:{nextUserStreamIndex:userStream.nextIdx(),nextSignalStreamsIndexes:t},timeout:12e4}).then(function(t){var n=t&&t.signalStreams&&t.signalStreams[e],r=ClientObjectStream(patchDiff);if(n)r.push(n);var i=r.lastObj();return i&&i.sevenSignal?i.sevenSignal:null})},'''
new_api = '''exp.requestSignalRefresh=function(){return getUpdateAsync()},'''
if s.count(old_api) != 1:
    raise SystemExit(f'Expected original requestSignalRefresh block once, found {s.count(old_api)}')
s = s.replace(old_api, new_api, 1)

old_cycle = '''t.attachChildView(m,[t.signalView,f]),a=function(){var e=o.model.getLastSignal(l);t.attachChildView(m,[t.signalView,e])},s=e.model.userDataUpdatedSubscription.subscribe(a),q=window.setInterval(function(){o.model.requestSignalRefresh(l).done(function(e){if(e)t.attachChildView(m,[t.signalView,e])})},60000),u.enhanceWithin(),n.each(t.postproc,function(e){e(u)})},r.detach=function(){s&&(s.stop(),s=null),q&&(window.clearInterval(q),q=null)}};'''
new_cycle = '''t.attachChildView(m,[t.signalView,f]),a=function(){var e=o.model.getLastSignal(l);t.attachChildView(m,[t.signalView,e])},s=e.model.userDataUpdatedSubscription.subscribe(a),v=function(){q&&(window.clearInterval(q),q=null)},b=function(){if(!document.hidden&&!q){o.model.requestSignalRefresh();q=window.setInterval(function(){document.hidden||o.model.requestSignalRefresh()},60000)}},w=function(){document.hidden?v():b()},b(),document.addEventListener("visibilitychange",w),window.addEventListener("focus",b),window.addEventListener("blur",v),t.$root.closest(".ui-page").on("pageshow.statusUpdate",b).on("pagehide.statusUpdate",v),u.enhanceWithin(),n.each(t.postproc,function(e){e(u)})},r.detach=function(){s&&(s.stop(),s=null),v&&v(),document.removeEventListener("visibilitychange",w),window.removeEventListener("focus",b),window.removeEventListener("blur",v),t.$root.closest(".ui-page").off(".statusUpdate"),q=null}};'''
if s.count(old_cycle) != 1:
    raise SystemExit(f'Expected original status timer block once, found {s.count(old_cycle)}')
s = s.replace(old_cycle, new_cycle, 1)

p.write_text(s, encoding='utf-8')
print('Patched Status to use the post-login getUpdateAsync request every 60s while focused/visible:', p)
