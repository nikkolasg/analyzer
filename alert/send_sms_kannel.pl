#!/usr/bin/perl

# syntax1: send_sms.sh <msisdn> "<text>"
# syntax2: echo -e "<message>" | ./send_sms.sh <msisdn> [<msisdn> ..]
# version 0.1, 2009-07-31, prepaid.services@orange.ch
# version 0.2, 2009-08-03, prepaid.services@orange.ch - reading input from pipe
# version 0.3, 2011-09-08, sending message through kannel

use Encode;
use URI::Escape;
use LWP::UserAgent;

$origin="PPS";
$host_port = "172.19.55.225:13013";
$uid = "tester";
$pwd = "foobar2";

#if tty -s <&1; then
if ( -t STDIN ) {
    @msisdn = ($ARGV[0]);
    shift @ARGV;
    $text = join(" ",@ARGV);
}
else {
    # reading from pipe
    # verbose=false;
    @msisdn=@ARGV;
    @lines = <STDIN> ;
    $text = join("",@lines);
}


my $browser = LWP::UserAgent->new;
$browser->agent('ReportsBot/1.01');

$browser->credentials(
  $host_port
  #,'httpServer'  # server realm
  #,'xss' => 'xss'
);

print "msisdns: " . join(", ",@msisdn) . "\n";
print "text: \n" . $text . "\n";

# now send the message
foreach my $m (@msisdn) {
    send_sms($m,$origin,$text);
}

exit;
# this is the sample command
# http://172.19.57.104:8085/authmtsmshttp?dest=%2B41787872747&src=PPS&destaddrnpi=1&destaddrton=1&srcaddrnpi=1&srcaddrton=5&body=This+is+a+test%0D%0Afrom+pps&registered=true&eventUrl=http%3A%2F%2F127.0.0.1%3A82%2Ftestwebserver

# === subs =========================================================================

sub send_sms {
    my $msisdn = shift;
    my $origin = shift;
    my $text   = shift;

    # http://172.19.55.228:13013/cgi-bin/sendsms?username=tester&password=foobar&to=0787872747&from=pps-kannel&text=Hello%20Mr.%0Aspecial%3A%20%C3%A9%C3%0APPS%20-%20kannel%20is%20working
    my $url = "http://" . $host_port . "/cgi-bin/sendsms";
    #url="http://172.19.55.228:13013/cgi-bin/sendsms"
    $url .= "?username=" . $uid ;
    $url .= "&password=" . $pwd ;  
    $url .= "&to=" . uri_escape($msisdn) ;
    $url .= "&from=" . uri_escape($origin) ;
    #$url .= "&destaddrnpi=1&destaddrton=1&srcaddrnpi=1&srcaddrton=5";
    $text =~ s/\\n/\n/g;  # to allow sending "\n" for newlines as well..
    $url .= "&text=" . uri_escape(encode("utf8",$text)) ;
    #(sms_encode "$(url_encode "$ltext")")
    #url=${url}"&body=line1%0D%0Aline2"
    #$url .= "&registered=true";
    #$url .= "&eventUrl=http%3A%2F%2F127.0.0.1%3A82%2Ftestwebserver" ;
    
    print "url: $url\n";
    my $response = $browser->get($url);
    print $response->header("Server"), "\n";
    print $response->content(), "\n";
}

