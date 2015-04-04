/**
 * Created by Konstantin on 03.04.2015.
 */
Ext.define('TorrentWatchList.view.tabs.TabController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.tab-view',

    onTabChange: function(tabs, newTab, oldTab) {
        Ext.suspendLayouts();
        console.log('chenge tab to ' + newTab.title);
        var grid = newTab.items.getAt(0).items.getAt(0);
        var store = grid.store

        store.load({ params: { hubid: grid.hub_id} });
        grid.getView().refresh();

        Ext.resumeLayouts(true);
    }
});