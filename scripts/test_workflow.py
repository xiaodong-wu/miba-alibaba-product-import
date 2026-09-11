"""Offline regression tests; synthetic data only, no live uploads or generation."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from compose_content import compose, company_profile, FIXED, split_faq, FRAME_OPEN, FRAME_CLOSE
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
                        images='https://i.ibb.co/a/cover.webp|Product on white')
        prefix = ('<section class="xb_import_v2"><h1>Xinbada Product</h1>'
                  '<p>Xinbada Industrial (Shenzhen) Group Co., Ltd.</p>'
                  '<img src="https://i.ibb.co/a/scene.webp" alt="Application" width="1200" height="800" loading="eager">'
                  '<p>Application concept visualization</p>' +
                  '<section class="xb_import_v2 miba_faq_section"><h2>FAQ</h2>' +
                  ''.join('<article class="xb_faq_item"><h2>Question</h2><p>Answer</p></article>' for _ in range(6)) + '</section></section>')
        self.detail = prefix
        self.review = {'rows': [{'row_number': 2, 'status': 'success',
                                'checks': {k: True for k in CHECKS}, 'evidence': 'evidence/test.json'}]}
        self.images = self.root / 'images'
        folder = self.images / 'xinbada-product'
        folder.mkdir(parents=True)
        records = []
        for name, role, size in [('cover', 'cover', (800, 800)), ('scene', 'scenario', (1200, 800))]:
            Image.new('RGB', size, 'white').save(folder / (name + '.webp'), 'WEBP')
            records.append({'file': name + '.webp', 'role': role, 'generated': True})
        uploaded = {'complete': True, 'uploaded': [
            {'file': 'cover.webp', 'direct_url': self.row['thumb']},
            {'file': 'scene.webp', 'direct_url': self.row['scenario_image']}]}
        for i in range(4):
            name = f'gallery-{i}.webp'
            Image.new('RGB', (800, 800), (i * 40, 60, 90)).save(folder / name, 'WEBP')
            records.append({'file': name, 'role': 'gallery', 'generated': True})
            url = 'https://i.ibb.co/a/' + name
            uploaded['uploaded'].append({'file': name, 'direct_url': url})
            self.row['images'] += '\n' + url + f'|Distinct product view {i}'
        for title, filename in FIXED:
            Image.new('RGB', (1000, 600), 'white').save(folder / filename, 'WEBP')
            records.append({'file': filename, 'role': 'supplied_static', 'title': title,
                            'generated': False, 'width': 1000, 'height': 600})
            url = 'https://i.ibb.co/a/' + filename
            uploaded['uploaded'].append({'file': filename, 'direct_url': url})
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

    def test_faq_follows_all_fixed_images(self):
        content = self.row['content']
        self.assertLess(content.index('miba-accessory-options.webp'), content.index('miba_faq_section'))
        self.assertTrue(content.endswith('</section>' + FRAME_CLOSE))

    def test_company_profile_is_before_fixed_images(self):
        content = self.row['content']
        self.assertIn(company_profile(), content)
        self.assertLess(content.index('<section class="xb_import_v2 miba_company_profile">'), content.index('miba_fixed_blocks'))
        self.assertIn('balance before shippment.', content)

    def test_company_copy_change_or_omission_is_rejected(self):
        original = self.row['content']
        for modified in [original.replace(company_profile(), ''),
                         original.replace('balance before shippment.', 'balance before shipment.')]:
            with self.subTest(modified_length=len(modified)):
                self.row['content'] = modified
                self.assertEqual(self.run_validation()['result'], 'failed')

    def test_duplicate_company_profile_is_rejected(self):
        self.row['content'] = self.row['content'].replace(company_profile(), company_profile() * 2)
        self.assertEqual(self.run_validation()['result'], 'failed')

    def test_faq_before_fixed_images_is_rejected(self):
        inner = self.row['content'][len(FRAME_OPEN):-len(FRAME_CLOSE)]
        body, faq = split_faq(inner)
        self.row['content'] = FRAME_OPEN + faq + body + FRAME_CLOSE
        self.assertEqual(self.run_validation()['result'], 'failed')

    def test_content_after_faq_is_rejected(self):
        self.row['content'] = self.row['content'][:-len(FRAME_CLOSE)] + '<p>Extra content</p>' + FRAME_CLOSE
        self.assertEqual(self.run_validation()['result'], 'failed')

    def test_pro_fields_preserves_real_csv_newlines_and_numbers(self):
        for newline in ['\n', '\r\n']:
            with self.subTest(newline=repr(newline)):
                self.row['pro_fields'] = newline.join([
                    '15W wireless output with compatible devices',
                    '7.5W output for a compatible device',
                    'Compact design for desks, with adjustable viewing',
                    'Logo printing in a "custom" finish'])
                self.assertEqual(self.run_validation()['errors'], [])
                with (self.root / 'output.csv').open(encoding='utf-8', newline='') as f:
                    self.assertEqual(next(csv.DictReader(f))['pro_fields'], self.row['pro_fields'])

    def test_pro_fields_rejects_list_markers(self):
        valid = self.row['pro_fields']
        for prefix in ['• ', '. ', '- ', '1. ', '(1) ', '|`-+#$&*|']:
            with self.subTest(prefix=prefix):
                self.row['pro_fields'] = prefix + valid
                self.assertTrue(any('pro_fields' in e['message'] for e in self.run_validation()['errors']))

    def test_pro_fields_rejects_wrong_entry_count(self):
        for count in [1, 3, 9]:
            self.row['pro_fields'] = '\n'.join(['Entry'] * count)
            self.assertTrue(any('pro_fields' in e['message'] for e in self.run_validation()['errors']))

    def test_detail_images_excluded_from_gallery(self):
        self.assertEqual(self.run_validation()['result'], 'passed')
        original_gallery = self.row['images']
        for url in [self.row['scenario_image'], 'https://i.ibb.co/a/factory-photo.webp']:
            self.row['images'] += '\n' + url + '|Not a product gallery image'
            self.assertEqual(self.run_validation()['result'], 'failed')
            self.row['images'] = original_gallery

    def test_unknown_detail_url_rejected(self):
        self.row['content'] = self.row['content'].replace('/a/scene.webp', '/a/unknown.webp')
        self.assertEqual(self.run_validation()['result'], 'failed')

    def test_width_larger_than_1400_rejected(self):
        self.row['content'] = self.row['content'].replace('max-width:1400px', 'max-width:1600px')
        self.assertEqual(self.run_validation()['result'], 'failed')

    def test_source_coverage_review_required(self):
        self.review['rows'][0]['checks']['source_coverage_reviewed'] = False
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
            {'source': 'raw.png', 'name': 'product-cover', 'role': 'cover', 'generated': True},
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

    def test_four_gallery_required_excluding_cover(self):
        manifest = self.images / 'xinbada-product.image-manifest.json'
        data = json.loads(manifest.read_text())
        data['images'] = [r for r in data['images'] if r['file'] != 'gallery-3.webp']
        manifest.write_text(json.dumps(data))
        (self.images / 'xinbada-product' / 'gallery-3.webp').unlink()
        upload = self.root / 'upload-manifests' / 'xinbada-product.json'
        u = json.loads(upload.read_text())
        u['uploaded'] = [r for r in u['uploaded'] if r['file'] != 'gallery-3.webp']
        upload.write_text(json.dumps(u))
        self.row['images'] = '\n'.join(self.row['images'].splitlines()[:-1])
        result = self.run_validation()
        self.assertTrue(any('at least four' in e['message'] for e in result['errors']))

    def test_all_gallery_and_cover_must_be_generated(self):
        manifest = self.images / 'xinbada-product.image-manifest.json'
        original = manifest.read_text()
        for role in ('cover', 'gallery'):
            data = json.loads(original)
            next(r for r in data['images'] if r['role'] == role)['generated'] = False
            manifest.write_text(json.dumps(data))
            self.assertTrue(any('provenance' in e['message'] for e in self.run_validation()['errors']))
        manifest.write_text(original)

    def test_preparation_rejects_ungenerated_cover(self):
        Image.new('RGB', (800, 800), 'white').save(self.root / 'raw.png')
        plan = self.root / 'bad-plan.json'
        for role in ('cover', 'gallery'):
            plan.write_text(json.dumps({'images': [{'source': 'raw.png', 'name': 'photo', 'role': role, 'generated': False}]}))
            with self.assertRaises(ValueError):
                prepare(plan, self.root / 'rejected-output')

    def test_richness_and_layout_review_required(self):
        for key in ('generated_gallery_verified', 'content_richness_reviewed', 'layout_reference_reviewed'):
            self.review['rows'][0]['checks'][key] = False
            self.assertEqual(self.run_validation()['result'], 'failed')
            self.review['rows'][0]['checks'][key] = True

    def test_large_multiline_csv_key_read(self):
        self.source_row['template'] = 'x' * 150_000 + '\r\n' + self.template
        self.run_validation()
        self.assertEqual(read_api_key(self.root / 'input.csv', 2), 'synthetic-test-key')


if __name__ == '__main__':
    unittest.main()
