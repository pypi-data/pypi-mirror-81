""" Classes for peppy.Project smoketesting """

from peppy import Project
from peppy.exceptions import MissingAmendmentError, InvalidSampleTableFileException
from peppy.const import SAMPLE_NAME_ATTR
from pandas import DataFrame
from yaml import safe_load, dump
import pytest
import os
import tempfile

__author__ = "Michal Stolarczyk"
__email__ = "michal@virginia.edu"

EXAMPLE_TYPES = \
    ["basic", "derive", "imply", "append", "amendments1", "amendments2",
     "derive_imply", "duplicate", "imports", "subtable1", "subtable2",
     "subtable3", "subtable4", "subtable5", "remove"]


def _get_pair_to_post_init_test(cfg_path):
    """

    :param cfg_path: path to the project config file
    :type cfg_path: str
    :return: list of two project objects to compare
    :rtype: list[peppy.Project]
    """
    p = Project(cfg=cfg_path)
    pd = Project(cfg=cfg_path, defer_samples_creation=True)
    pd.create_samples()
    return [p, pd]


def _cmp_all_samples_attr(p1, p2, attr):
    """
    Compare a selected attribute values for all samples in two Projects

    :param p1: project to comapre
    :type p1: peppy.Project
    :param p2: project to comapre
    :type p2: peppy.Project
    :param attr: attribute name to compare
    :type attr: str
    """

    assert [getattr(s, attr, None) for s in p1.samples] == \
           [getattr(s, attr, None) for s in p2.samples]


class ProjectConstructorTests:
    def test_empty(self):
        """ Verify that an empty Project instance can be created """
        p = Project()
        assert isinstance(p, Project)
        assert len(p.samples) == 0

    def test_nonexistent(self):
        """ Verify that OSError is thrown when config does not exist """
        with pytest.raises(OSError):
            Project(cfg="nonexistentfile.yaml")

    @pytest.mark.parametrize('defer', [False, True])
    @pytest.mark.parametrize('example_pep_cfg_path', EXAMPLE_TYPES, indirect=True)
    def test_instantiaion(self, example_pep_cfg_path, defer):
        """
        Verify that Project object is successfully created for every example PEP
        """
        p = Project(cfg=example_pep_cfg_path, defer_samples_creation=defer)
        assert isinstance(p, Project)

    @pytest.mark.parametrize('defer', [False, True])
    @pytest.mark.parametrize('example_pep_cfg_path', ["amendments1"], indirect=True)
    def test_amendments(self, example_pep_cfg_path, defer):
        """
        Verify that the amendment is activate at object instantiation
        """
        p = Project(cfg=example_pep_cfg_path, amendments="newLib", defer_samples_creation=defer)
        assert all([s["protocol"] == "ABCD" for s in p.samples])

    @pytest.mark.parametrize('defer', [False, True])
    @pytest.mark.parametrize('example_pep_cfg_path', ["old"], indirect=True)
    def test_old_format_support(self, example_pep_cfg_path, defer):
        """
        Verify that old format (without implications and subprojects)
        is still supported
        """
        os.environ["DATA"] = "data"
        p = Project(cfg=example_pep_cfg_path, defer_samples_creation=defer)
        assert all(["read1" in s for s in p.samples])

    @pytest.mark.parametrize('example_pep_cfg_path', ["subtable1"], indirect=True)
    def test_subsample_table_works_when_no_sample_mods(self, example_pep_cfg_path):
        """
        Verify that subsample table functionality is not
        dependant on sample modifiers
        """
        p = Project(cfg=example_pep_cfg_path)
        assert any([s["file"] != "multi" for s in p.samples])

    @pytest.mark.parametrize('example_pep_cfg_path', ["subtables"], indirect=True)
    def test_subsample_table_multiple(self, example_pep_cfg_path):
        """
        Verify that subsample table functionality in multi subsample context
        """
        p = Project(cfg=example_pep_cfg_path)
        assert any(["desc" in s for s in p.samples])

    @pytest.mark.parametrize('defer', [False, True])
    @pytest.mark.parametrize('example_pep_cfg_path', EXAMPLE_TYPES, indirect=True)
    def test_no_description(self, example_pep_cfg_path, defer):
        """
        Verify that Project object is successfully created when no description
         is specified in the config
        """
        p = Project(cfg=example_pep_cfg_path, defer_samples_creation=defer)
        assert isinstance(p, Project)
        assert "description" in p and p.description is None

    @pytest.mark.parametrize('defer', [False, True])
    @pytest.mark.parametrize('desc', ["desc1",
                                      "desc 2 <test> 123$!@#;11",
                                      11,
                                      None])
    @pytest.mark.parametrize('example_pep_cfg_path', EXAMPLE_TYPES, indirect=True)
    def test_description(self, example_pep_cfg_path, desc, defer):
        """
        Verify that Project object contains description specified in the config
        """
        td = tempfile.mkdtemp()
        temp_path_cfg = os.path.join(td, "config.yaml")
        with open(example_pep_cfg_path, 'r') as f:
            data = safe_load(f)
        data["description"] = desc
        del data["sample_table"]
        with open(temp_path_cfg, 'w') as f:
            dump(data, f)
        p = Project(cfg=temp_path_cfg, defer_samples_creation=defer)
        assert isinstance(p, Project)
        assert "description" in p and p.description == str(desc)

    @pytest.mark.parametrize('example_pep_cfg_noname_path',
                             ["project_config.yaml"], indirect=True)
    def test_missing_sample_name_derive(self, example_pep_cfg_noname_path):
        """
        Verify that even if sample_name column is missing in the sample table,
        it can be derived and no error is issued
        """
        p = Project(cfg=example_pep_cfg_noname_path)
        assert SAMPLE_NAME_ATTR in p.sample_table.columns

    @pytest.mark.parametrize('example_pep_cfg_noname_path',
                             ["project_config_noname.yaml"], indirect=True)
    def test_missing_sample_name(self, example_pep_cfg_noname_path):
        """
        Verify that if sample_name column is missing in the sample table an
        error is issued
        """
        with pytest.raises(InvalidSampleTableFileException):
            Project(cfg=example_pep_cfg_noname_path)

    @pytest.mark.parametrize('example_pep_cfg_noname_path',
                             ["project_config_noname.yaml"], indirect=True)
    def test_missing_sample_name_defer(self, example_pep_cfg_noname_path):
        """
        Verify that if sample_name column is missing in the sample table an
        error is not issued if sample creation is deferred
        """
        Project(cfg=example_pep_cfg_noname_path, defer_samples_creation=True)

    @pytest.mark.parametrize('example_pep_cfg_noname_path',
                             ["project_config_noname.yaml"], indirect=True)
    def test_missing_sample_name_custom_index(self, example_pep_cfg_noname_path):
        """
        Verify that if sample_name column is missing in the sample table an
        error is not issued if a custom sample_table index is set
        """
        p = Project(cfg=example_pep_cfg_noname_path, sample_table_index="id")
        assert p.sample_name_colname == "id"


class ProjectManipulationTests:
    @pytest.mark.parametrize('example_pep_cfg_path', ["amendments1"], indirect=True)
    def test_amendments_activation_interactive(self, example_pep_cfg_path):
        """
        Verify that the amendment can be activated interactively
        """
        p = Project(cfg=example_pep_cfg_path)
        p.activate_amendments("newLib")
        assert all([s["protocol"] == "ABCD" for s in p.samples])
        assert p.amendments is not None

    @pytest.mark.parametrize('example_pep_cfg_path', ["amendments1"], indirect=True)
    def test_amendments_deactivation_interactive(self, example_pep_cfg_path):
        """
        Verify that the amendment can be activated interactively
        """
        p = Project(cfg=example_pep_cfg_path)
        p.deactivate_amendments()
        assert all([s["protocol"] != "ABCD" for s in p.samples])
        p.activate_amendments("newLib")
        p.deactivate_amendments()
        assert all([s["protocol"] != "ABCD" for s in p.samples])
        assert p.amendments is None

    @pytest.mark.parametrize('defer', [False, True])
    @pytest.mark.parametrize('example_pep_cfg_path', ["amendments1"], indirect=True)
    def test_missing_amendment_raises_error(self, example_pep_cfg_path, defer):
        """
        Verify that the missing amendment request raises correct exception
        """
        with pytest.raises(MissingAmendmentError):
            Project(cfg=example_pep_cfg_path, amendments="nieznany", defer_samples_creation=defer)

    @pytest.mark.parametrize('defer', [False, True])
    @pytest.mark.parametrize('example_pep_cfg_path', ["amendments1"], indirect=True)
    def test_missing_amendment_raises_error(self, example_pep_cfg_path, defer):
        """
        Verify that the amendments argument cannot be null
        """
        p = Project(cfg=example_pep_cfg_path, defer_samples_creation=defer)
        with pytest.raises(TypeError):
            p.activate_amendments(amendments=None)

    @pytest.mark.parametrize('defer', [False, True])
    @pytest.mark.parametrize('example_pep_cfg_path', EXAMPLE_TYPES, indirect=True)
    def test_str_repr_correctness(self, example_pep_cfg_path, defer):
        """
        Verify string representation correctness
        """
        p = Project(cfg=example_pep_cfg_path, defer_samples_creation=defer)
        str_repr = p.__str__()
        assert example_pep_cfg_path in str_repr
        assert "{} samples".format(str(len(p.samples))) in str_repr
        assert p.name in str_repr

    @pytest.mark.parametrize('defer', [False, True])
    @pytest.mark.parametrize('example_pep_cfg_path', ["amendments1"], indirect=True)
    def test_amendments_listing(self, example_pep_cfg_path, defer):
        p = Project(cfg=example_pep_cfg_path, defer_samples_creation=defer)
        assert isinstance(p.list_amendments, list)

    @pytest.mark.parametrize('example_pep_cfg_path', ["basic"], indirect=True)
    def test_sample_updates_regenerate_df(self, example_pep_cfg_path):
        """
        Verify that Sample modifications cause sample_table regeneration
        """
        p = Project(cfg=example_pep_cfg_path)
        s_ori = p.sample_table
        p.samples[0].update({"witam": "i_o_zdrowie_pytam"})
        assert not p.sample_table.equals(s_ori)

    @pytest.mark.parametrize('example_pep_cfg_path', ["subtable1"], indirect=True)
    def test_subsample_table_property(self, example_pep_cfg_path):
        """
        Verify that Sample modifications cause sample_table regeneration
        """
        p = Project(cfg=example_pep_cfg_path)
        assert isinstance(p.subsample_table, DataFrame) \
               or isinstance(p.subsample_table, list)

    @pytest.mark.parametrize('example_pep_cfg_path', ["basic"], indirect=True)
    def test_get_sample(self, example_pep_cfg_path):
        """ Verify that sample getting method works """
        p = Project(cfg=example_pep_cfg_path)
        p.get_sample(sample_name=p.samples[0]["sample_name"])

    @pytest.mark.parametrize('example_pep_cfg_path', ["basic"], indirect=True)
    def test_get_sample_nonexistent(self, example_pep_cfg_path):
        """ Verify that sample getting returns ValueError if not sample found """
        p = Project(cfg=example_pep_cfg_path)
        with pytest.raises(ValueError):

            p.get_sample(sample_name="kdkdkdk")


class SampleModifiersTests:
    @pytest.mark.parametrize('example_pep_cfg_path', ["append"], indirect=True)
    def test_append(self, example_pep_cfg_path):
        """ Verify that the appended attribute is added to the samples """
        p = Project(cfg=example_pep_cfg_path)
        assert all([s["read_type"] == "SINGLE" for s in p.samples])

    @pytest.mark.parametrize('example_pep_cfg_path', ["imports"], indirect=True)
    def test_imports(self, example_pep_cfg_path):
        """ Verify that the imported attribute is added to the samples """
        p = Project(cfg=example_pep_cfg_path)
        assert all([s["imported_attr"] == "imported_val" for s in p.samples])

    @pytest.mark.parametrize('example_pep_cfg_path', ["imply"], indirect=True)
    def test_imply(self, example_pep_cfg_path):
        """
        Verify that the implied attribute is added to the correct samples
        """
        p = Project(cfg=example_pep_cfg_path)
        assert all([s["genome"] == "hg38" for s in p.samples if
                    s["organism"] == "human"])
        assert all([s["genome"] == "mm10" for s in p.samples if
                    s["organism"] == "mouse"])

    @pytest.mark.parametrize('example_pep_cfg_path', ["duplicate"], indirect=True)
    def test_duplicate(self, example_pep_cfg_path):
        """
        Verify that the duplicated attribute is identical to the original
        """
        p = Project(cfg=example_pep_cfg_path)
        assert all([s["organism"] == s["animal"] for s in p.samples])

    @pytest.mark.parametrize('example_pep_cfg_path', ["derive"], indirect=True)
    def test_derive(self, example_pep_cfg_path):
        """
        Verify that the declared attr derivation happened
        """
        p = Project(cfg=example_pep_cfg_path)
        assert all(["file_path" in s for s in p.samples])
        assert all(["file_path" in s["_derived_cols_done"] for s in p.samples])

    @pytest.mark.parametrize('example_pep_cfg_path', ["remove"], indirect=True)
    def test_remove(self, example_pep_cfg_path):
        """
        Verify that the declared attr was eliminated from every sample
        """
        p = Project(cfg=example_pep_cfg_path)
        assert all(["protocol" not in s for s in p.samples])

    @pytest.mark.parametrize('example_pep_cfg_path', ["subtable2"], indirect=True)
    def test_subtable(self, example_pep_cfg_path):
        """
        Verify that the sample merging takes place
        """
        p = Project(cfg=example_pep_cfg_path)
        assert all([isinstance(s["file"], list) for s in p.samples
                    if s["sample_name"] in ["frog_1", "frog2"]])


class PostInitSampleCreationTests:
    @pytest.mark.parametrize('example_pep_cfg_path', ["append"], indirect=True)
    def test_append(self, example_pep_cfg_path):
        """
        Verify that the appending works the same way in a post init
        sample creation scenario
        """
        p, pd = _get_pair_to_post_init_test(example_pep_cfg_path)
        _cmp_all_samples_attr(p, pd, "read_type")

    @pytest.mark.parametrize('example_pep_cfg_path', ["imports"], indirect=True)
    def test_imports(self, example_pep_cfg_path):
        """
        Verify that the importing works the same way in a post init
        sample creation scenario
        """
        p, pd = _get_pair_to_post_init_test(example_pep_cfg_path)
        _cmp_all_samples_attr(p, pd, "imported_attr")

    @pytest.mark.parametrize('example_pep_cfg_path', ["imply"], indirect=True)
    def test_imply(self, example_pep_cfg_path):
        """
        Verify that the implication the same way in a post init
        sample creation scenario
        """
        p, pd = _get_pair_to_post_init_test(example_pep_cfg_path)
        _cmp_all_samples_attr(p, pd, "genome")

    @pytest.mark.parametrize('example_pep_cfg_path', ["duplicate"], indirect=True)
    def test_duplicate(self, example_pep_cfg_path):
        """
        Verify that the duplication the same way in a post init
        sample creation scenario
        """
        p, pd = _get_pair_to_post_init_test(example_pep_cfg_path)
        _cmp_all_samples_attr(p, pd, "organism")

    @pytest.mark.parametrize('example_pep_cfg_path', ["derive"], indirect=True)
    def test_derive(self, example_pep_cfg_path):
        """
        Verify that the derivation the same way in a post init
        sample creation scenario
        """
        p, pd = _get_pair_to_post_init_test(example_pep_cfg_path)
        _cmp_all_samples_attr(p, pd, "file_path")
