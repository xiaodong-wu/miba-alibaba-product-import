"""Offline regression tests; synthetic data only, no live uploads or generation."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from compose_content import compose, FIXED
from prepare_images import prepare
from validate_output import validate, REQUIRED, CHECKS
from upload_images_to_imgbb import read_api_key


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.headers = sorted(REQUIRED) + ['custom_field', 'template']
        self.template = '<style>.legacy{color:red}</style>\r\n<div class="legacy">Company section</div>\r\n'
        self.source_row = {f: '' for f in self.headers}
        self.source_row.update(link='https://www.alibaba.com/product-detail/example.html',
                               template=self.template, IMGBB_API_KEY='synthetic-test-key',
                               custom_field='unchanged, "quoted"\r\ntext')
        self.row = self.source_row.copy()
        self.row.update(title='Xinbada Product for Daily Use', remark='Verified product description.',
                        file_name='xinbada-product', pro_fields='One\nTwo\nThree\nFour',
                        seo_title1='Custom Product for Everyday Applications | Xinbada OEM',
                        seo_desc='Xinbada offers this product for verified applications with private label support.',
                        thumb='https://i.ibb.co/a/cover.webp',
                        scenario_image='https://i.ibb.co/a/scene.webp',
                        images='https://i.ibb.co/a/cover.webp|Product on white\nhttps://i.ibb.co/a/scene.webp|Product application concept')
        prefix = ('<section class="xb_import_v2"><h1>Xinbada Product</h1>'
                  '<p>Xinbada Industrial (Shenzhen) Group Co., Ltd.</p>'
                  '<img src="https://i.ibb.co/a/scene.webp" alt="Application" width="1200" height="800" loading="eager">'
                  '<p>Application concept visualization</p>' +
                  ''.join('<article class="xb_faq_item"><h2>Question</h2><p>Answer</p></article>' for _ in range(6)) + '</section>')
        self.detail = prefix
        self.review = {'rows': [{'row_number': 2, 'status': 'success',
                                'checks': {k: True for k in CHECKS}, 'evidence': 'evidence/test.json'}]}
        self.images = self.root / 'images'
        folder = self.images / 'xinbada-product'
        folder.mkdir(parents=True)
        records = []
        for name, role, size in [('cover', 'cover', (800, 800)), ('scene', 'scenario', (1200, 800))]:
            Image.new('RGB', size, 'white').save(folder / (name + '.webp'), 'WEBP')
            records.append({'file': name + '.webp', 'role': role, 'generated': role == 'scenario'})
        uploaded = {'complete': True, 'uploaded': [
            {'file': 'cover.webp', 'direct_url': self.row['thumb']},
            {'file': 'scene.webp', 'direct_url': self.row['scenario_image']}]}
        for title, filename in FIXED:
            Image.new('RGB', (1000, 600), 'white').save(folder / filename, 'WEBP')
            records.append({'file': filename, 'role': 'supplied_static', 'title': title,
                            'generated': False, 'width': 1000, 'height': 600})
            url = 'https://i.ibb.co/a/' + filename
            uploaded['uploaded'].append({'file': filename, 'direct_url': url})
            self.row['images'] += '\n' + url + '|' + title
        self.row['content'] = compose(self.detail, records, uploaded)
        (self.images / 'xinbada-product.image-manifest.json').write_text(json.dumps({'images': records}))
        uploads = self.root / 'upload-manifests'
        uploads.mkdir()
        (uploads / 'xinbada-product.json').write_text(json.dumps(uploaded))

    def run_validation(self):
        for filename, row in [('input.csv', self.source_row), ('output.csv', self.row)]:
            with (self.root / filename).open('w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
                writer.writerow(row)
        return validate(self.root / 'input.csv', self.root / 'output.csv', self.images, self.review)

    def test_valid_with_fixed_blocks(self):
        result = self.run_validation()
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['result'], 'passed')
        self.assertNotIn(self.template, self.row['content'])
        self.assertIn('<h2>Factory Photo</h2>', self.row['content'])

    def test_wrong_fixed_title_rejected(self):
        self.row['content'] = self.row['content'].replace('<h2>Factory Photo</h2>', '<h2>Changed</h2>')
        self.assertEqual(self.run_validation()['result'], 'failed')

    def test_template_column_not_required(self):
        self.headers.remove('template')
        del self.source_row['template']
        del self.row['template']
        self.assertEqual(self.run_validation()['result'], 'passed')

    def test_missing_fixed_block_rejected(self):
        self.row['content'] = self.detail
        self.assertEqual(self.run_validation()['result'], 'failed')

    def test_wrong_fixed_image_order_rejected(self):
        self.row['content'] = self.row['content'].replace('factory-photo.webp', 'temporary.webp').replace(
            'miba-logo-options.webp', 'factory-photo.webp').replace('temporary.webp', 'miba-logo-options.webp')
        self.assertEqual(self.run_validation()['result'], 'failed')

    def test_neutral_brand_without_company_name(self):
        self.row['title'] = 'Product for Daily Use'
        self.row['seo_title1'] = 'Custom Product for Everyday Applications and Projects'
        self.row['seo_desc'] = 'A product for verified everyday applications.'
        self.row['content'] = self.row['content'].replace('Xinbada Product', 'Product').replace(
            '<p>Xinbada Industrial (Shenzhen) Group Co., Ltd.</p>', '')
        self.assertEqual(self.run_validation()['result'], 'passed')

    def test_user_supplied_other_brand(self):
        self.row['title'] = 'Acme Product for Daily Use'
        self.row['content'] = self.row['content'].replace('Xinbada', 'Acme')
        self.row['seo_title1'] = 'Custom Product for Everyday Applications | Acme Brand'
        self.row['seo_desc'] = 'Acme product for verified applications.'
        self.assertEqual(self.run_validation()['result'], 'passed')

    def test_unknown_column_and_secret_preserved(self):
        self.row['custom_field'] = 'changed'
        self.row['IMGBB_API_KEY'] = 'other-synthetic-key'
        result = self.run_validation()
        self.assertEqual(result['result'], 'failed')
        self.assertNotIn('synthetic', json.dumps(result))

    def test_blocked_row_is_partial(self):
        self.row = self.source_row.copy()
        self.review['rows'][0] = {'row_number': 2, 'status': 'blocked', 'reason': 'Template conflict'}
        self.assertEqual(self.run_validation()['result'], 'partial')

    def test_seo_limit(self):
        self.row['seo_desc'] = 'x' * 141
        self.assertEqual(self.run_validation()['result'], 'failed')

    def test_source_image_cannot_be_new_detail(self):
        self.row['content'] = self.row['content'].replace('src="https://i.ibb.co/a/scene.webp"', 'src="https://i.ibb.co/a/cover.webp"')
        self.assertEqual(self.run_validation()['result'], 'failed')

    def test_image_preparation(self):
        Image.new('RGBA', (1600, 1000), (50, 100, 150, 150)).save(self.root / 'raw.png')
        plan = self.root / 'plan.json'
        plan.write_text(json.dumps({'images': [
            {'source': 'raw.png', 'name': 'product-cover', 'role': 'cover'},
            {'source': 'raw.png', 'name': 'application-concept', 'role': 'scenario', 'generated': True, 'width': 1200}]}))
        target = self.root / 'prepared'
        results = prepare(plan, target)
        self.assertEqual((results[0]['width'], results[0]['height']), (800, 800))
        self.assertEqual(results[1]['width'], 1200)
        with Image.open(target / 'product-cover.webp') as img:
            self.assertEqual(img.format, 'WEBP')
            self.assertIn('A', img.getbands())
        with self.assertRaises(ValueError):
            prepare(plan, target)

    def test_supplied_static_preserves_dimensions_and_title(self):
        Image.new('RGB', (900, 1300), 'white').save(self.root / 'Factory Photo.png')
        plan = self.root / 'fixed-plan.json'
        plan.write_text(json.dumps({'images': [{'source': 'Factory Photo.png',
            'name': 'factory-photo', 'role': 'supplied_static', 'generated': False}]}))
        records = prepare(plan, self.root / 'fixed-output')
        self.assertEqual((records[0]['width'], records[0]['height']), (900, 1300))
        self.assertEqual(records[0]['title'], 'Factory Photo')
        self.assertEqual(records[0]['quality'], 82)
        self.assertEqual(len(records[0]['source_sha256']), 64)
        self.assertFalse(records[0]['generated'])

    def test_large_multiline_csv_key_read(self):
        self.source_row['template'] = 'x' * 150_000 + '\r\n' + self.template
        self.run_validation()
        self.assertEqual(read_api_key(self.root / 'input.csv', 2), 'synthetic-test-key')


if __name__ == '__main__':
    unittest.main()
