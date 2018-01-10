def format_time(secs):
	m, s = divmod(secs, 60)
	if m <= 0:
		return "%i" % s
	else:
		h, m = divmod(m, 60)
		if h <= 0:
			return "%i:%02i" % (m, s)
		else:
			return "%i:%02i:%02i" % (h, m, s)
