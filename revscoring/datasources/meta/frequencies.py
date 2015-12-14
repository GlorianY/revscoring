from ..datasource import Datasource


class table(Datasource):
    """
    Generates a frequency table for a list of items generated by another
    datasource.

    :Parameters:
        items_datasource : :class:`revscoring.Datasource`
            A datasource that generates a list of some `hashable` item
        name : `str`
            A name for the datasource.
    """
    def __init__(self, items_datasource, name=None):
        name = self._format_name(name, [items_datasource])
        super().__init__(name, self.process,
                         depends_on=[items_datasource])

    def process(self, items):

        freq = {}
        for item in items:
            if item in freq:
                freq[item] += 1
            else:
                freq[item] = 1

        return freq


class delta(Datasource):
    """
    Generates a frequency table diff by comparing two frequency tables.

    :Parameters:
        old_ft_datasource : :class:`revscoring.Datasource`
            A frequency table datasource
        new_ft_datasource : :class:`revscoring.Datasource`
            A frequency table datasource
        name : `str`
            A name for the datasource.
    """
    def __init__(self, old_ft_datasource, new_ft_datasource, name=None):
        name = self._format_name(name, [old_ft_datasource, new_ft_datasource])
        super().__init__(name, self.process,
                         depends_on=[old_ft_datasource, new_ft_datasource])

    def process(self, old_ft, new_tf):
        old_ft = old_ft or {}

        delta_table = {}
        for item, new_count in new_tf.items():
            old_count = old_ft.get(token, 0)
            if new_count != old_count:
                delta_table[item] = new_count - old_count

        for item in old_ft.keys() - new_tf.keys():
            delta_table[item] = old_ft[item] * -1

        return delta_table


class prop_delta(Datasource):
    """
    Generates a proportional frequency table diff by comparing a
    frequency table diff with an old frequency table.

    :Parameters:
        old_ft_datasource : :class:`revscoring.Datasource`
            A frequency table datasource
        new_ft_datasource : :class:`revscoring.Datasource`
            A frequency table datasource
        name : `str`
            A name for the datasource.
    """
    def __init__(self, old_ft_datasource, ft_diff_datasource, name=None):
        name = self._format_name(name, [old_ft_datasource, ft_diff_datasource])
        super().__init__(name, self.process,
                         depends_on=[old_ft_datasource, ft_diff_datasource])

    def process(self, old_tf, ft_diff):
        prop_delta = {}
        for item, delta in ft_diff.items():
            prop_delta[item] = delta / old_tf.get(item, 1)

        return prop_delta
