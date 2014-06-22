	(function(d,s, id){
         var js, fjs = d.getElementsByTagName(s)[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement(s); js.id = id;
         js.src = "//connect.facebook.net/en_US/sdk.js";
         fjs.parentNode.insertBefore(js, fjs);
       }(document, 'script', 'facebook-jssdk'));

	function fblogin(){
		FB.getLoginStatus(function(response){
			if(response.status === 'connected'){
				console.log('Logged in.');
				if(response.status === 'not_authorized'){
				FB.login(function(){},
					{scope: 'user_friends,read_friendlists,read_stream'
				});
				}else{
					//do nothing
				};
			}else{
				FB.login(function(){},
					{scope: 'user_friends,read_friendlists,read_stream'
				});
			}
		});
		
	}

	function fblogout(){
		FB.logout(function(response) {
  	// user is now logged out
	});
	}