function dialogSubmitter(rq_type,tbl) {
	            $('#savedata').click(  function (event) {
				event.preventDefault();
				$("#popupForm").validate();
				if ($("#popupForm").valid()) {
					 var sendData={};
					 var id='';

					  $('#popupForm').serializeArray().map(function(item) {
						if(item.name=="id") id=item.value;
						else {
							if ( sendData[item.name] ) {
								if ( typeof(sendData[item.name]) === "string" ) {
									sendData[item.name] = [sendData[item.name]];
								}
								sendData[item.name].push(item.value);
							} else {
								sendData[item.name] = item.value;
							}
						}
					});

					if(id==''){
						method='POST';
						api_url= '/api/'+rq_type+'s';
					} else {
						method='PUT';
						api_url= '/api/'+rq_type+'/'+id;
					}
					$.ajax({
						url: api_url,
						type: method,
						data: sendData,
						dataType: "json",
						success: function () {
							console.log('saved');
							tbl.ajax.reload();
							$dialog.dialog('destroy').remove();
						},
						fail: function(xhr, textStatus, errorThrown){
						    console.log(xhr);
						    console.log(textStatus);
						    console.log(errorThrown);
                           			    alert('request failed');
			                        }
					});
                }
            });
}

function multiselector(elm){
elm.multiSelect({
  selectableHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='try \"12\"'>",
  selectionHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='try \"4\"'>",
  afterInit: function(ms){
    var that = this,
        $selectableSearch = that.$selectableUl.prev(),
        $selectionSearch = that.$selectionUl.prev(),
        selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
        selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';

    that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
    .on('keydown', function(e){
      if (e.which === 40){
        that.$selectableUl.focus();
        return false;
      }
    });

    that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
    .on('keydown', function(e){
      if (e.which == 40){
        that.$selectionUl.focus();
        return false;
      }
    });
  },
  afterSelect: function(){
    this.qs1.cache();
    this.qs2.cache();
  },
  afterDeselect: function(){
    this.qs1.cache();
    this.qs2.cache();
  }
});
}