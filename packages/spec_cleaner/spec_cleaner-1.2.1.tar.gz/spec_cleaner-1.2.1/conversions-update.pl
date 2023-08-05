#!/usr/bin/env perl

my $value = shift(@ARGV);
while (<STDIN>) {
	if (m@<location href=".+?/(.*)-.+?-.+?\.rpm"/>@) {
		$name = $1;
		next;
	}

	$start = m@^\s*<rpm:provides>@;
	$end = m@^\s*</rpm:provides>@;
	if ($start .. $end) {
		push @provides, $1
			if m@^\s*<rpm:entry name="$value\((.+?)\)".*?/>@;
	}
	if ($end && @provides) {
		$uniq{"$name: " . join(' ', @provides) . " \n"} = 1;
		undef @provides;
	}
}
print for (sort keys %uniq);
