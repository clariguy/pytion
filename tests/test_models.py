from pytion.models import *


class TestProperty:
    def test_create(self):
        p = Property.create(type_="multi_select", name="multiselected")
        p.get()
        assert p.id is None
        assert p.type == "multi_select"
        assert p.to_delete is False

    def test_create__to_rename(self):
        p = Property.create(name="renamed")
        p.get()
        assert p.id is None
        assert p.type == ""
        assert p.name == "renamed"
        assert p.to_delete is False

    def test_create__to_delete(self):
        p = Property.create(type_=None)
        p.get()
        assert p.id is None
        assert p.type is None
        assert p.to_delete is True

    def test_create__relation_single(self):
        p = Property.create("relation", single_property="878d628488d94894ab14f9b872cd6870")
        p.get()
        assert p.id is None
        assert p.type == "relation"
        assert p.to_delete is False
        assert isinstance(p.relation, LinkTo)
        assert p.relation.uri == "databases"
        assert p.subtype == "single_property"

    def test_create__relation_dual(self):
        p = Property.create("relation", dual_property="878d628488d94894ab14f9b872cd6870")
        p.get()
        assert p.id is None
        assert p.type == "relation"
        assert p.to_delete is False
        assert isinstance(p.relation, LinkTo)
        assert p.relation.uri == "databases"
        assert p.subtype == "dual_property"

    def test_create__status(self):
        p = Property.create("status")
        p_dict = p.get()
        assert p.id is None
        assert p.type == "status"
        assert p.to_delete is False
        assert isinstance(p.options, list)
        assert isinstance(p.groups, list)
        assert bool(p_dict["status"]) is False


class TestPropertyValue:
    def test_create__status(self):
        pv = PropertyValue.create("status", value="Done")
        p_dict = pv.get()
        assert pv.id is None
        assert pv.type == "status"
        assert p_dict["status"]["name"] == "Done"

    def test_create__relation(self):
        pv = PropertyValue.create("relation", value=[LinkTo.create(page_id="04262843082a478d97f741948a32613c")])
        p_dict = pv.get()
        assert pv.id is None
        assert pv.type == "relation"
        assert pv.has_more is False
        assert p_dict["relation"][0]["id"] == "04262843082a478d97f741948a32613c"


class TestBlock:
    def test_get__heading_1(self, no):
        block_id = "15a5790980db4e8798b9b7801385afbb"
        block = no.blocks.get(block_id)
        assert isinstance(block.obj, Block)
        assert isinstance(block.obj.text, RichTextArray)
        assert block.obj.type == "heading_1"
        assert block.obj.simple == "Block with heading 1 type"
        assert str(block.obj) == "# Block with heading 1 type"
        assert block.obj.has_children is False
        assert block.obj.is_toggleable is False

    def test_get__t_heading_1(self, no):
        block_id = "a62985febcac499f95e5b59643df6180"
        block = no.blocks.get(block_id)
        assert isinstance(block.obj, Block)
        assert isinstance(block.obj.text, RichTextArray)
        assert block.obj.type == "heading_1"
        assert block.obj.simple == "Block with Toggle Heading 1 type with no children"
        assert str(block.obj) == "# Block with Toggle Heading 1 type with no children"
        assert block.obj.has_children is False
        assert block.obj.is_toggleable is True

    def test_get__t_heading_2(self, no):
        block_id = "4b265c74e7644affad13a3820e208b78"
        block = no.blocks.get(block_id)
        assert isinstance(block.obj, Block)
        assert isinstance(block.obj.text, RichTextArray)
        assert block.obj.type == "heading_2"
        assert block.obj.simple == "Block with Toggle Heading 2 type with children"
        assert str(block.obj) == "## Block with Toggle Heading 2 type with children"
        assert block.obj.has_children is True
        assert block.obj.is_toggleable is True

    def test_create__heading_1(self):
        b = Block.create("hello there", type_="heading_1")
        b_dict = b.get()
        assert b.id == ""
        assert b.type == "heading_1"
        assert b_dict["heading_1"]["is_toggleable"] is False

    def test_create__t_heading_2(self):
        b = Block.create("hello there", type_="heading_2", is_toggleable=True)
        b_dict = b.get()
        assert b.id == ""
        assert b.type == "heading_2"
        assert b_dict["heading_2"]["is_toggleable"] is True
